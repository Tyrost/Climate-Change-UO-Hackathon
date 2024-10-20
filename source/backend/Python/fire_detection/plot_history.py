import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def plot_history(log_dir):
    """Plots training and validation metrics."""
    metrics_file = os.path.join(log_dir, 'training_logs', 'version_0', 'metrics.csv')
    df = pd.read_csv(metrics_file)

    # Filter out rows without 'epoch' (e.g., steps)
    df = df.dropna(subset=['epoch'])

    # Remove duplicates and sort by epoch
    df = df.drop_duplicates(subset=['epoch']).sort_values('epoch')
    epochs = df['epoch'].values

    # Plot accuracy
    if 'train_acc_epoch' in df.columns or 'val_acc_epoch' in df.columns:
        if 'train_acc_epoch' in df.columns:
            plt.plot(epochs, df['train_acc_epoch'], label='Training Accuracy')
        if 'val_acc_epoch' in df.columns:
            plt.plot(epochs, df['val_acc_epoch'], label='Validation Accuracy')
        plt.legend()
        plt.grid()
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.savefig(os.path.join(log_dir, "accuracy.png"), dpi=300, bbox_inches='tight')
        plt.clf()

    # Plot loss
    if 'train_loss_epoch' in df.columns or 'val_loss_epoch' in df.columns:
        if 'train_loss_epoch' in df.columns:
            plt.plot(epochs, df['train_loss_epoch'], label='Training Loss')
        if 'val_loss_epoch' in df.columns:
            plt.plot(epochs, df['val_loss_epoch'], label='Validation Loss')
        plt.legend()
        plt.grid()
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.savefig(os.path.join(log_dir, "loss.png"), dpi=300, bbox_inches='tight')
        plt.clf()

    # Plot Dice Coefficient
    if 'train_dice_epoch' in df.columns or 'val_dice_epoch' in df.columns:
        if 'train_dice_epoch' in df.columns:
            plt.plot(epochs, df['train_dice_epoch'], label='Training Dice Coefficient')
        if 'val_dice_epoch' in df.columns:
            plt.plot(epochs, df['val_dice_epoch'], label='Validation Dice Coefficient')
        plt.legend()
        plt.grid()
        plt.xlabel('Epochs')
        plt.ylabel('Dice Coefficient')
        plt.savefig(os.path.join(log_dir, "dice_coefficient.png"), dpi=300, bbox_inches='tight')
        plt.clf()
