import torch
from torch import nn
from torch.nn import functional as F


class SELayer(nn.Module):
    def __init__(self, channel=32, reduction=8):
        super(SELayer, self).__init__()
        self.cse_avg_pool = nn.AdaptiveAvgPool3d(1)
        self.cse_fc = nn.Sequential(
            nn.Linear(channel, channel // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channel // reduction, channel, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, z, w, h = x.size()
        cse_y = self.cse_avg_pool(x).view(b, c)
        cse_y = self.cse_fc(cse_y).view(b, c, 1, 1, 1)

        return x * cse_y.expand_as(x)
