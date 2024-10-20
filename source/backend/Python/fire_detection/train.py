import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import torch
from torch.utils.data import DataLoader

from generator import ImageMaskDataset
from model_module import SegmentationModel
from plot_history import plot_history

from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import CSVLogger
import pytorch_lightning as pl

# Set parameters
PLOT_HISTORY = True
MASK_ALGORITHM = 'Kumar-Roy'
N_FILTERS = 16
N_CHANNELS = 3
EPOCHS = 50
BATCH_SIZE = 64
IMAGE_SIZE = (256, 256)
MODEL_NAME = 'unet'
RANDOM_STATE = 42
IMAGES_PATH = '/home/anishd/carbs/anishd/data/images/patches/'
MASKS_PATH = '/home/anishd/carbs/anishd/data/masks/patches/'
IMAGES_DATAFRAME = './dataset/images_masks.csv'
OUTPUT_DIR = '/home/anishd/carbs/anishd/data/train_output/'
WORKERS = 4
EARLY_STOP_PATIENCE = 5
CHECKPOINT_PERIOD = 5
CHECKPOINT_MODEL_NAME = f'checkpoint-{MODEL_NAME}-{MASK_ALGORITHM}-epoch_{{epoch:02d}}'
INITIAL_EPOCH = 0
RESTART_FROM_CHECKPOINT = None
if INITIAL_EPOCH > 0:
    RESTART_FROM_CHECKPOINT = os.path.join(OUTPUT_DIR, f'checkpoint-{MODEL_NAME}-{MASK_ALGORITHM}-epoch_{INITIAL_EPOCH:02d}.ckpt')
FINAL_WEIGHTS_OUTPUT = f'model_{MODEL_NAME}_{MASK_ALGORITHM}_final_weights.ckpt'
CUDA_DEVICE = 0
LEARNING_RATE = 1e-3  # Added learning rate parameter

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Set device
device = torch.device(f'cuda:{CUDA_DEVICE}' if torch.cuda.is_available() else 'cpu')

# Read image and mask paths from CSV files
df = pd.read_csv(IMAGES_DATAFRAME, header=None, names=['images', 'masks'])
x_train = pd.read_csv('./dataset/images_train.csv', header=0, names=['images'])
y_train = pd.read_csv('./dataset/masks_train.csv', header=0, names=['masks'])
x_val = pd.read_csv('./dataset/images_val.csv', header=0, names=['images'])
y_val = pd.read_csv('./dataset/masks_val.csv', header=0, names=['masks'])

print(f"Base path: {IMAGES_PATH}")
print(f"First image: {x_train['images'].iloc[0]}")  # Print the first image file name

# Map the images and mask paths
images_train = [os.path.join(IMAGES_PATH, image) for image in x_train['images']]
masks_train = [os.path.join(MASKS_PATH, mask) for mask in y_train['masks']]
images_validation = [os.path.join(IMAGES_PATH, image) for image in x_val['images']]
masks_validation = [os.path.join(MASKS_PATH, mask) for mask in y_val['masks']]

# Create datasets and dataloaders
train_dataset = ImageMaskDataset(images_train, masks_train, image_mode="762")
val_dataset = ImageMaskDataset(images_validation, masks_validation, image_mode="762")
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=WORKERS)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=WORKERS)

# Initialize model
model = SegmentationModel(
    model_name=MODEL_NAME,
    n_classes=1,
    input_channels=N_CHANNELS,
    n_filters=N_FILTERS,
    lr=LEARNING_RATE  # Pass learning rate to the model
)

# Set up callbacks
checkpoint_callback = ModelCheckpoint(
    dirpath=OUTPUT_DIR,
    filename=CHECKPOINT_MODEL_NAME,
    save_top_k=1,
    monitor='val_loss',
    mode='min'
)
early_stop_callback = EarlyStopping(
    monitor='val_loss',
    patience=EARLY_STOP_PATIENCE,
    mode='min'
)
logger = CSVLogger(save_dir=OUTPUT_DIR, name='training_logs')

# Initialize trainer
trainer = pl.Trainer(
    max_epochs=EPOCHS,
    callbacks=[checkpoint_callback, early_stop_callback],
    accelerator='gpu' if torch.cuda.is_available() else 'cpu',
    devices=[CUDA_DEVICE] if torch.cuda.is_available() else None,
    logger=logger
)

# Start training
if RESTART_FROM_CHECKPOINT:
    trainer.fit(model, train_loader, val_loader,ckpt_path=RESTART_FROM_CHECKPOINT)
else:
    trainer.fit(model, train_loader, val_loader)
print('Train finished!')

# Save the final model weights
print('Saving weights')
model_weights_output = os.path.join(OUTPUT_DIR, FINAL_WEIGHTS_OUTPUT)
trainer.save_checkpoint(model_weights_output)
print(f"Weights Saved: {model_weights_output}")

# Plot training history
if PLOT_HISTORY:
    plot_history(OUTPUT_DIR)
