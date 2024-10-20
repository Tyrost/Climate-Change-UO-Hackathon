import torch
import torch.nn as nn
import pytorch_lightning as pl
from torch.nn import functional as F
from typing import Optional

# Define a reusable Conv2D block
class Conv2DBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, batchnorm=True):
        super(Conv2DBlock, self).__init__()
        layers = []
        # First convolution
        layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, padding=kernel_size//2))
        if batchnorm:
            layers.append(nn.BatchNorm2d(out_channels))
        layers.append(nn.ReLU(inplace=True))
        # Second convolution
        layers.append(nn.Conv2d(out_channels, out_channels, kernel_size=kernel_size, padding=kernel_size//2))
        if batchnorm:
            layers.append(nn.BatchNorm2d(out_channels))
        layers.append(nn.ReLU(inplace=True))
        self.conv = nn.Sequential(*layers)

    def forward(self, x):
        return self.conv(x)

# Fully Convolutional Network (FCN) Model
class FCN(pl.LightningModule):
    def __init__(self, nClasses=1, input_height=256, input_width=256, 
                 n_filters=16, dropout=0.1, batchnorm=True, n_channels=3):
        super(FCN, self).__init__()
        self.save_hyperparameters()
        self.nClasses = nClasses

        # Block 1
        self.block1_conv1 = nn.Conv2d(n_channels, n_filters, kernel_size=3, padding=1)
        self.block1_bn1 = nn.BatchNorm2d(n_filters) if batchnorm else nn.Identity()
        self.block1_conv2 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1)
        self.block1_bn2 = nn.BatchNorm2d(n_filters) if batchnorm else nn.Identity()

        # Block 2
        self.block2_conv1 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1)
        self.block2_bn1 = nn.BatchNorm2d(n_filters) if batchnorm else nn.Identity()
        self.block2_conv2 = nn.Conv2d(n_filters, n_filters, kernel_size=3, padding=1)
        self.block2_bn2 = nn.BatchNorm2d(n_filters) if batchnorm else nn.Identity()

        # Output layer
        self.out = nn.Conv2d(n_filters, nClasses, kernel_size=3, padding=1)
        self.out_activation = nn.ReLU()  # Keras used 'relu' activation

    def forward(self, x):
        # Block 1
        x = F.relu(self.block1_bn1(self.block1_conv1(x)))
        x = F.relu(self.block1_bn2(self.block1_conv2(x)))
        f1 = x  # Feature map after Block 1

        # Block 2
        x = F.relu(self.block2_bn1(self.block2_conv1(x)))
        x = F.relu(self.block2_bn2(self.block2_conv2(x)))
        f2 = x  # Feature map after Block 2

        # Output
        o = self.out(x)
        o = self.out_activation(o)
        return o


# Standard U-Net Model
class UNet(pl.LightningModule):
    def __init__(self, nClasses=1, input_height=256, input_width=256, 
                 n_filters=16, dropout=0.1, batchnorm=True, n_channels=3):
        super(UNet, self).__init__()
        self.save_hyperparameters()
        self.nClasses = nClasses

        # Contracting Path
        self.c1 = Conv2DBlock(n_channels, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.p1 = nn.MaxPool2d(2)
        self.d1 = nn.Dropout(dropout)

        self.c2 = Conv2DBlock(n_filters * 1, n_filters * 2, kernel_size=3, batchnorm=batchnorm)
        self.p2 = nn.MaxPool2d(2)
        self.d2 = nn.Dropout(dropout)

        self.c3 = Conv2DBlock(n_filters * 2, n_filters * 4, kernel_size=3, batchnorm=batchnorm)
        self.p3 = nn.MaxPool2d(2)
        self.d3 = nn.Dropout(dropout)

        self.c4 = Conv2DBlock(n_filters * 4, n_filters * 8, kernel_size=3, batchnorm=batchnorm)
        self.p4 = nn.MaxPool2d(2)
        self.d4 = nn.Dropout(dropout)

        self.c5 = Conv2DBlock(n_filters * 8, n_filters * 16, kernel_size=3, batchnorm=batchnorm)

        # Expansive Path
        self.u6 = nn.ConvTranspose2d(n_filters * 16, n_filters * 8, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c6 = Conv2DBlock(n_filters * 16, n_filters * 8, kernel_size=3, batchnorm=batchnorm)
        self.d6 = nn.Dropout(dropout)

        self.u7 = nn.ConvTranspose2d(n_filters * 8, n_filters * 4, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c7 = Conv2DBlock(n_filters * 8, n_filters * 4, kernel_size=3, batchnorm=batchnorm)
        self.d7 = nn.Dropout(dropout)

        self.u8 = nn.ConvTranspose2d(n_filters * 4, n_filters * 2, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c8 = Conv2DBlock(n_filters * 4, n_filters * 2, kernel_size=3, batchnorm=batchnorm)
        self.d8 = nn.Dropout(dropout)

        self.u9 = nn.ConvTranspose2d(n_filters * 2, n_filters * 1, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c9 = Conv2DBlock(n_filters * 2, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.d9 = nn.Dropout(dropout)

        self.out = nn.Conv2d(n_filters * 1, self.nClasses, kernel_size=1)
        self.out_activation = nn.Sigmoid()  

    def forward(self, x):
        # Contracting Path
        c1 = self.c1(x)
        p1 = self.p1(c1)
        d1 = self.d1(p1)

        c2 = self.c2(d1)
        p2 = self.p2(c2)
        d2 = self.d2(p2)

        c3 = self.c3(d2)
        p3 = self.p3(c3)
        d3 = self.d3(p3)

        c4 = self.c4(d3)
        p4 = self.p4(c4)
        d4 = self.d4(p4)

        c5 = self.c5(d4)

        # Expansive Path
        u6 = self.u6(c5)
        u6 = torch.cat([u6, c4], dim=1)
        u6 = self.d6(u6)
        c6 = self.c6(u6)

        u7 = self.u7(c6)
        u7 = torch.cat([u7, c3], dim=1)
        u7 = self.d7(u7)
        c7 = self.c7(u7)

        u8 = self.u8(c7)
        u8 = torch.cat([u8, c2], dim=1)
        u8 = self.d8(u8)
        c8 = self.c8(u8)

        u9 = self.u9(c8)
        u9 = torch.cat([u9, c1], dim=1)
        u9 = self.d9(u9)
        c9 = self.c9(u9)

        output = self.out(c9)
        output = self.out_activation(output)
        return output

# U-Net Small Variant 1
class UNetSmall1(pl.LightningModule):
    def __init__(self, nClasses=1, input_height=256, input_width=256, 
                 n_filters=16, dropout=0.1, batchnorm=True, n_channels=3):
        super(UNetSmall1, self).__init__()
        self.save_hyperparameters()
        self.nClasses = nClasses

        # Contracting Path
        self.c1 = Conv2DBlock(n_channels, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.p1 = nn.MaxPool2d(2)
        self.d1 = nn.Dropout(dropout)

        self.c2 = Conv2DBlock(n_filters * 1, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.p2 = nn.MaxPool2d(2)
        self.d2 = nn.Dropout(dropout)

        self.c3 = Conv2DBlock(n_filters * 1, n_filters * 2, kernel_size=3, batchnorm=batchnorm)

        # Expansive Path
        self.u8 = nn.ConvTranspose2d(n_filters * 2, n_filters * 1, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c8 = Conv2DBlock(n_filters * 1 + n_filters *1, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.d8 = nn.Dropout(dropout)

        self.u9 = nn.ConvTranspose2d(n_filters * 1, n_filters * 1, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c9 = Conv2DBlock(n_filters * 1 + n_filters *1, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.d9 = nn.Dropout(dropout)

        self.out = nn.Conv2d(n_filters * 1, self.nClasses, kernel_size=1)
        self.out_activation = nn.ReLU()  # Keras used 'relu' activation

    def forward(self, x):
        # Contracting Path
        c1 = self.c1(x)
        p1 = self.p1(c1)
        d1 = self.d1(p1)

        c2 = self.c2(d1)
        p2 = self.p2(c2)
        d2 = self.d2(p2)

        c3 = self.c3(d2)

        # Expansive Path
        u8 = self.u8(c3)
        u8 = torch.cat([u8, c2], dim=1)
        u8 = self.d8(u8)
        c8 = self.c8(u8)

        u9 = self.u9(c8)
        u9 = torch.cat([u9, c1], dim=1)
        u9 = self.d9(u9)
        c9 = self.c9(u9)

        output = self.out(c9)
        output = self.out_activation(output)
        return output

# U-Net Small Variant 2
class UNetSmall2(pl.LightningModule):
    def __init__(self, nClasses=1, input_height=256, input_width=256, 
                 n_filters=16, dropout=0.1, batchnorm=True, n_channels=3):
        super(UNetSmall2, self).__init__()
        self.save_hyperparameters()
        self.nClasses = nClasses

        # Contracting Path
        self.c1 = Conv2DBlock(n_channels, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.p1 = nn.MaxPool2d(2)
        self.d1 = nn.Dropout(dropout)

        self.c2 = Conv2DBlock(n_filters * 1, n_filters * 4, kernel_size=3, batchnorm=batchnorm)
        self.d2 = nn.Dropout(dropout)  # No pooling after c2 in Keras code

        # Expansive Path
        self.u3 = nn.ConvTranspose2d(n_filters * 4, n_filters * 1, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.c3 = Conv2DBlock(n_filters * 1 + n_filters *1, n_filters * 1, kernel_size=3, batchnorm=batchnorm)
        self.d3 = nn.Dropout(dropout)

        self.out = nn.Conv2d(n_filters * 1, self.nClasses, kernel_size=1)
        self.out_activation = nn.ReLU()  # Keras used 'relu' activation

    def forward(self, x):
        # Contracting Path
        c1 = self.c1(x)
        p1 = self.p1(c1)
        d1 = self.d1(p1)

        c2 = self.c2(d1)
        d2 = self.d2(c2)  # No pooling after c2

        # Expansive Path
        u3 = self.u3(d2)
        u3 = torch.cat([u3, c1], dim=1)
        u3 = self.d3(u3)
        c3 = self.c3(u3)

        output = self.out(c3)
        output = self.out_activation(output)
        return output

# Model Factory to select models based on name
def get_model(model_name, nClasses=1, input_height=256, input_width=256, 
             n_filters=16, dropout=0.1, batchnorm=True, n_channels=3):
    model_name = model_name.lower()
    print(f"Creating model: {model_name}")
    if model_name == 'fcn':
        return FCN(
            nClasses=nClasses,
            input_height=input_height,
            input_width=input_width,
            n_filters=n_filters,
            dropout=dropout,
            batchnorm=batchnorm,
            n_channels=n_channels
        )
    elif model_name == 'unet':
        return UNet(
            nClasses=nClasses,
            input_height=input_height,
            input_width=input_width,
            n_filters=n_filters,
            dropout=dropout,
            batchnorm=batchnorm,
            n_channels=n_channels
        )
    elif model_name == 'unet_small':
        return UNetSmall1(
            nClasses=nClasses,
            input_height=input_height,
            input_width=input_width,
            n_filters=n_filters,
            dropout=dropout,
            batchnorm=batchnorm,
            n_channels=n_channels
        )
    elif model_name == 'unet_smaller':
        return UNetSmall2(
            nClasses=nClasses,
            input_height=input_height,
            input_width=input_width,
            n_filters=n_filters,
            dropout=dropout,
            batchnorm=batchnorm,
            n_channels=n_channels
        )
    else:
        raise ValueError(f"Unknown model name: {model_name}")
