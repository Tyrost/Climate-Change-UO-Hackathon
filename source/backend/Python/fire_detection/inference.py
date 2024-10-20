import logging
from datetime import datetime, timedelta
import torch
from pathlib import Path
import numpy as np
from process_landsat import open_landsat, login, download_scene, search
import os
import rasterio
import matplotlib.pyplot as plt
from model_module import SegmentationModel  

# Parameters
MODEL_PATH = '/home/anishd/carbs/anishd/data/train_output/model_unet_Kumar-Roy_final_weights.ckpt'  # Path to the trained model
MAX_PIXEL_VALUE = 65535 
N_CHANNELS = 3 
N_FILTERS = 16  
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
OUTPUT_PATH = '/home/anishd/hackuo/outputs/'       # Directory to save output masks

def get_img_arr(path):
    """Reads image and normalizes it."""
    img = rasterio.open(path).read().transpose((1, 2, 0))
    img = np.float32(img) / MAX_PIXEL_VALUE
    return img

# Load model
model = SegmentationModel.load_from_checkpoint(
    MODEL_PATH, model_name='unet', n_classes=1, input_channels=N_CHANNELS, n_filters=N_FILTERS)
model.eval()  
model.to(DEVICE)

# Configure logging
logging.basicConfig(level=logging.INFO)

def find_nearest_scene(lat, lon, target_date, cloud_cover):
    """
    Searches for a scene nearest to the given target date.
    If no scene is found for the exact date, it looks for scenes close to that date.
    """
    scenes = search(
        lat=lat, lon=lon,
        start_date=(target_date - timedelta(days=30)).strftime('%Y-%m-%d'),
        end_date=(target_date + timedelta(days=30)).strftime('%Y-%m-%d'),
        cloud_cover=cloud_cover
    )

    if not scenes:
        logging.error(f"No scenes found near {target_date}.")
        return None

    # Find the scene closest to the target date
    selected_scene = min(
        scenes, key=lambda scene: abs(scene['acquisition_date'] - target_date))
    logging.info(
        f"Found scene {selected_scene['landsat_product_id']} for date {selected_scene['acquisition_date'].strftime('%Y-%m-%d')}")
    return selected_scene

def landsat_qa(pixel_map):
    """Quality assurance mask for Landsat data."""
    mask = (pixel_map == 21824) | (pixel_map == 21888) | (pixel_map == 21952)
    return mask

def process_scene(scene_path, lat, lon, image_size):
    """
    Process the downloaded scene and extract relevant data using open_landsat.
    """
    try:
        data_dict = open_landsat(scene_path, lat, lon, image_size)
        qa = '' #landsat_qa(data_dict['QA_PIXEL'])

        # Select relevant bands
        data_keys = ['B7', 'B6', 'B2']
        out_data = np.concatenate(
            [data_dict[b][:, :, None] for b in data_keys], axis=-1)

        return out_data[None, :, :, :], qa
    except Exception as e:
        logging.error(f"Failed to process scene at {scene_path}: {e}")
        return None, None

def download_and_process_scene(lat, lon, target_date, output_dir, ee, image_size=256):
    """
    Downloads and processes the scene for the given lat/lon and date, returning the image tensor.
    Only downloads if the scene is not already available locally.
    """
    # Set the cloud cover threshold
    cloud_cover = 10

    # Find the nearest scene to the target date
    scene = find_nearest_scene(lat, lon, target_date, cloud_cover)
    if scene is None:
        return None

    scene_filename = f"{scene['landsat_product_id']}.tar"
    scene_path = output_dir / scene_filename

    # Download the scene if it's not already downloaded
    if not scene_path.exists():
        logging.info(f"Downloading scene {scene['landsat_product_id']}")
        download_scene(ee,scene['entity_id'], output_dir=str(output_dir))
    else:
        logging.info(f"Scene already exists: {scene['landsat_product_id']}")

    # Process the scene to extract the image
    image_tensor, qa_mask = process_scene(scene_path, lat, lon, image_size)
    if image_tensor is None:
        logging.error(f"Failed to process scene {scene['landsat_product_id']}")
        return None

    return image_tensor  # Shape: [1, H, W, C]

def main(lat, lon, date_str):
    # Parse the input date
    target_date = datetime.strptime(date_str, '%Y-%m-%d')

    # Define the download directory
    download_dir = Path('/home/anishd/carbs/anishd/landsat_downloads')
    download_dir.mkdir(parents=True, exist_ok=True)

    # Login
    ee = login()

    try:
        # Download and process the scene
        image_tensor = download_and_process_scene(
            lat, lon, target_date, download_dir, ee)

        if image_tensor is not None:
            logging.info(
                f"Returning image tensor of shape {image_tensor.shape} for the date {date_str}.")
            return image_tensor
        else:
            logging.error(
                f"Could not retrieve image for the given date: {date_str}")
            return None
    finally:
        ee.logout()
        # Logout
    # ee.logout()

def save_mask(mask, output_path):
    """Save the predicted mask as a TIFF file."""
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Save the mask
    with rasterio.open(
        output_path, 'w', driver='GTiff',
        height=mask.shape[0], width=mask.shape[1],
        count=1, dtype=mask.dtype
    ) as dst:
        dst.write(mask, 1)

def predict_fire(image_tensor, date_str, fire_threshold=0.01, output_folder=OUTPUT_PATH):
    """
    Predicts whether there is fire in the given image tensor.
    Fire is considered detected if at least fire_threshold proportion of pixels are classified as fire.
    Also saves the predicted segmentation mask.

    Args:
        image_tensor: The input image tensor of shape [1, H, W, C].
        date_str: String representing the date, used for naming output files.
        fire_threshold: The proportion of pixels that need to be classified as fire to consider fire detected.
        output_folder: The folder to save the output mask.

    Returns:
        has_fire: Boolean indicating whether fire is detected.
    """
    # image_tensor is numpy array of shape [1, H, W, C]
    original_image = image_tensor.squeeze(0)  # Now shape [H, W, C]
    image_tensor = original_image.astype(np.float32)
    image_tensor = image_tensor / MAX_PIXEL_VALUE  # Normalize
    image_tensor = torch.from_numpy(image_tensor).float()
    image_tensor = image_tensor.permute(2, 0, 1)  # C x H x W
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension: [1, C, H, W]
    image_tensor = image_tensor.to(DEVICE)

    with torch.no_grad():
        output = model(image_tensor)
        # output shape: [1, n_classes, H, W]
        output_mask = output.squeeze(0).squeeze(0)  # Now shape [H, W]
        # print("Output mask", output_mask)
        # output_mask_prob = torch.sigmoid(output_mask)  # Apply sigmoid activation
        output_mask_prob = output_mask.cpu().numpy()
        # print("Output mask prob", output_mask_prob)
        # print("Output mask prob", output_mask_prob)
        output_mask_binary = np.logical_not(output_mask_prob > 0.09)  # Threshold to get binary mask

    # Calculate the percentage of pixels classified as fire
    fire_pixel_ratio = np.mean(output_mask_binary)

    # Fire is detected if the ratio of fire pixels exceeds the threshold
    has_fire = fire_pixel_ratio >= fire_threshold

    # Save the predicted probability mask
    output_mask_path = os.path.join(output_folder, f"pred_{date_str}.tif")
    save_mask((output_mask_prob * 255).astype(np.uint8), output_mask_path)

    # Save the binary mask
    binary_mask_path = os.path.join(output_folder, f"pred_{date_str}_binary.tif")
    save_mask(output_mask_binary.astype(np.uint8) * 255, binary_mask_path)

    # Save intermediate visualizations as images
    # Save the original image
    original_image_path = os.path.join(output_folder, f"original_{date_str}.png")
    plt.imsave(original_image_path, original_image / np.max(original_image))  # Normalize the original image

    # Save the predicted binary mask
    predicted_mask_path = os.path.join(output_folder, f"pred_mask_{date_str}.png")
    plt.imsave(predicted_mask_path, output_mask_binary, cmap='gray')

    # Save the output mask before sigmoid
    output_before_sigmoid_path = os.path.join(output_folder, f"output_before_sigmoid_{date_str}.png")
    plt.imsave(output_before_sigmoid_path, output_mask.cpu().numpy(), cmap='hot')

    # Save the output mask probability after sigmoid
    output_after_sigmoid_path = os.path.join(output_folder, f"output_after_sigmoid_{date_str}.png")
    plt.imsave(output_after_sigmoid_path, output_mask_prob, cmap='hot')

    return has_fire


def check_fire(lat, lon, date_str):
    """Checks if there is fire in the image corresponding to the given location and date."""
    image_tensor = main(lat, lon, date_str)
    print("Got image tensor... Now predicting fire...")
    if image_tensor is not None:
        has_fire = predict_fire(image_tensor, date_str)
        return has_fire
    else:
        # Handle the case where image_tensor is None
        logging.error("No image data available to predict fire.")
        return False

if __name__ == "__main__":
    # lat = 42.3528 #36.1777 #42.3528
    # lat = 37.8545
    lat = 56.7233
    # lon = -121.8053 #-120.2026 #121.8053
    # lon = -120.0863
    lon = -111.3803
    # date_str = '2021-07-30' #'2018-06-15'  # 2021-07-06
    # date_str = '2013-09-17'
    date_str = '2016-05-03'
    has_fire = check_fire(lat, lon, date_str)
    print(f"Fire detected: {has_fire}")
