import torch

# def dice_coef(y_true, y_pred, smooth=1e-6):
#     """Calculates the Dice Coefficient."""
#     y_true_f = y_true.view(-1)
#     y_pred_f = y_pred.view(-1)
#     intersection = (y_true_f * y_pred_f).sum()
#     dice = (2. * intersection + smooth) / (y_true_f.sum() + y_pred_f.sum() + smooth)
#     return dice

def dice_coef(y_true, y_pred, smooth=1e-6):
    intersection = (y_true * y_pred).sum()
    union = y_true.sum() + y_pred.sum()
    dice = (2. * intersection + smooth) / (union + smooth)
    return dice


def soft_dice_loss(y_true, y_pred, smooth=1):
    # Flatten the tensors
    y_true_f = y_true.view(-1)
    y_pred_f = y_pred.view(-1)
    intersection = (y_true_f * y_pred_f).sum()
    return 1 - (2. * intersection + smooth) / (y_true_f.sum() + y_pred_f.sum() + smooth)

def tversky_coef(y_true, y_pred, alpha=0.5, beta=0.5, smooth=1e-6):
    # Flatten the tensors to avoid issues with dimensions
    y_true_flat = y_true.view(-1)
    y_pred_flat = y_pred.view(-1)
    
    # True positives, false positives, and false negatives
    true_pos = (y_true_flat * y_pred_flat).sum()
    false_neg = (y_true_flat * (1 - y_pred_flat)).sum()
    false_pos = ((1 - y_true_flat) * y_pred_flat).sum()
    
    # Tversky coefficient calculation
    tversky_index = (true_pos + smooth) / (true_pos + alpha * false_pos + beta * false_neg + smooth)
    
    return tversky_index

def tversky_loss(y_true, y_pred, alpha=0.5, beta=0.5):
    # The loss is 1 - Tversky index
    return 1 - tversky_coef(y_true, y_pred, alpha, beta)