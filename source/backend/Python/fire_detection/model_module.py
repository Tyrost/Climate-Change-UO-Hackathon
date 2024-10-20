import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from models import get_model
from metrics import dice_coef, tversky_loss

class SegmentationModel(pl.LightningModule):
    """PyTorch Lightning module for segmentation."""
    def __init__(self, model_name='fcn', n_classes=1, input_channels=3, n_filters=16, lr=1e-4):
        super(SegmentationModel, self).__init__()
        self.model = get_model(model_name, nClasses=n_classes, input_height=256, input_width=256,  n_filters=n_filters, dropout=0.1, batchnorm=True, n_channels=3)
        self.lr = lr
        self.n_classes = n_classes

    def forward(self, x):
        return self.model(x)

    # def compute_loss(self, y_pred, y_true):
    #     bce_loss = F.binary_cross_entropy(y_pred, y_true)
    #     dice_loss = 1 - dice_coef(y_true, y_pred)  
    #     combined_loss = 0.5*bce_loss + 0.5*dice_loss 
    #     return combined_loss
    def compute_loss(self, y_pred, y_true):
        # Binary Cross-Entropy Loss
        bce_loss = F.binary_cross_entropy(y_pred, y_true)
        # Tversky Loss
        tv_loss = tversky_loss(y_true, y_pred, 0.3, 0.7)
        # Combine the two
        combined_loss = 0.5 * bce_loss + 0.5 * tv_loss
        return combined_loss
    
    def training_step(self, batch, batch_idx):
        x, y = batch
        # print("X and Y shapes")
        # print(x.shape, y.shape)
        # print("X and Y")
        # print(x)
        # print(y)
        y_pred = self.forward(x)
        loss = self.compute_loss(y_pred, y)
        self.log('train_loss', loss, prog_bar=True)

        # Binarize predictions and ground truth
        pred_binary = (y_pred > 0.5).float()
        y_binary = (y > 0.5).float()

        # print(pred_binary.shape, y_binary.shape)
        # print(pred_binary)
        # print(y_binary)

        # Compute metrics
        accuracy = (pred_binary == y_binary).float().mean()
        dice = dice_coef(y_binary, pred_binary)
        self.log('train_acc', accuracy, prog_bar=True)
        self.log('train_dice', dice, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_pred = self.forward(x)
        loss = self.compute_loss(y_pred, y)
        self.log('val_loss', loss, prog_bar=True)

        # Binarize predictions and ground truth
        pred_binary = (y_pred > 0.5).float()
        y_binary = (y > 0.5).float()

        # print(pred_binary.shape, y_binary.shape)
        # print(pred_binary)
        # print(y_binary)

        # Compute metrics
        accuracy = (pred_binary == y_binary).float().mean()
        dice = dice_coef(y_binary, pred_binary)
        self.log('val_acc', accuracy, prog_bar=True)
        self.log('val_dice', dice, prog_bar=True)
        return loss


    # def training_step(self, batch, batch_idx):
    #     x, y = batch
    #     y_pred = self.forward(x)
    #     loss = self.compute_loss(y_pred, y)
    #     self.log('train_loss', loss, prog_bar=True)
    #     # Compute metrics
    #     pred_binary = (y_pred > 0.5).float()
    #     accuracy = (pred_binary == y).float().mean()
    #     dice = dice_coef(y, pred_binary)
    #     self.log('train_acc', accuracy, prog_bar=True)
    #     self.log('train_dice', dice, prog_bar=True)
    #     return loss

    # def validation_step(self, batch, batch_idx):
    #     x, y = batch
    #     y_pred = self.forward(x)
    #     loss = self.compute_loss(y_pred, y)
    #     self.log('val_loss', loss, prog_bar=True)
    #     # Compute metrics
    #     pred_binary = (y_pred > 0.5).float()
    #     accuracy = (pred_binary == y).float().mean()
    #     dice = dice_coef(y, pred_binary)
    #     self.log('val_acc', accuracy, prog_bar=True)
    #     self.log('val_dice', dice, prog_bar=True)
    #     return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.lr)
        return optimizer
