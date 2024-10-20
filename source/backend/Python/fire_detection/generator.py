import os
import numpy as np
import rasterio
from torch.utils.data import Dataset
import torch

MAX_PIXEL_VALUE = 65535  # Max pixel value for normalization

def get_img_arr(path):
    """Reads image and normalizes it."""
    img = rasterio.open(path).read().transpose((1, 2, 0))
    img = np.float32(img) / MAX_PIXEL_VALUE
    return img

def get_img_762bands(path):
    """Reads specific bands (7,6,2) and normalizes them."""
    img = rasterio.open(path).read((7, 6, 2)).transpose((1, 2, 0))
    img = np.float32(img) / MAX_PIXEL_VALUE
    return img

def get_mask_arr(path):
    """Reads mask and normalizes it."""
    img = rasterio.open(path).read(1)
    seg = np.float32(img)
    seg = seg / seg.max()  # Normalize mask to [0, 1]
    seg = np.expand_dims(seg, axis=0)  # Add channel dimension
    return seg

class ImageMaskDataset(Dataset):
    """PyTorch Dataset for image and mask pairs."""
    def __init__(self, images_path, masks_path, transform=None, image_mode='10bands'):
        self.images_path = images_path
        self.masks_path = masks_path
        self.transform = transform
        self.image_mode = image_mode
        if self.image_mode == '762':
            self.read_image_fn = get_img_762bands
        else:
            self.read_image_fn = get_img_arr

    def __len__(self):
        return len(self.images_path)

    def __getitem__(self, idx):
        img_path = self.images_path[idx]
        mask_path = self.masks_path[idx]

        image = self.read_image_fn(img_path)
        mask = get_mask_arr(mask_path)

        # Convert to torch tensors and rearrange dimensions
        image = torch.from_numpy(image).permute(2, 0, 1).float()  # C x H x W
        mask = torch.from_numpy(mask).float()  # 1 x H x W

        if self.transform:
            image = self.transform(image)
            mask = self.transform(mask)

        return image, mask
