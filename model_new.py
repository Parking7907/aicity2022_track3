import torch
import torch.nn as nn
import torch.nn.functional as F
import pdb
from efficientnet_pytorch import EfficientNet
from model_utils.attention_modules import Spatial_Attention
from model_utils.attention_modules import Temporal_Attention


class NEW_MYNET(nn.Module):
    def __init__(self, sequence_size):
        super().__init__()
        self.sequence_size = sequence_size
        self.motion_features = Spatial_Attention(sequence_size)
        self.backbone = EfficientNet.from_pretrained('efficientnet-b0', in_channels=3)
        self.TA = Temporal_Attention(n_segment=sequence_size//3, feature_dim=1000, num_class=20)
        
    def forward(self, rgb):
        B = rgb.shape[0]
        PA = self.motion_features(rgb)
        #rgb Shape = 16 31 3 224 224
        #encoded features = rgb[:, 1:, ...] => 16, 30, 3, 224, 224
        #encoded_features = rgb[:,1:,...]*PA
        backbone_out = self.backbone(rgb.mean(2).reshape(-1, 3, 320, 320))
        temporal_vec = (backbone_out).reshape(B, self.sequence_size//3, -1)
        return self.TA(temporal_vec)

class NEW_MYNET_224(nn.Module):
    def __init__(self, sequence_size):
        super().__init__()
        self.sequence_size = sequence_size
        self.motion_features = Spatial_Attention(sequence_size)
        self.backbone = EfficientNet.from_pretrained('efficientnet-b0', in_channels=3)
        self.TA = Temporal_Attention(n_segment=sequence_size//3, feature_dim=1000, num_class=20)
        
    def forward(self, rgb):
        B = rgb.shape[0]
        PA = self.motion_features(rgb)
        #rgb Shape = 16 31 3 224 224
        #encoded features = rgb[:, 1:, ...] => 16, 30, 3, 224, 224
        #encoded_features = rgb[:,1:,...]*PA
        backbone_out = self.backbone(rgb.mean(2).reshape(-1, 3, 224, 224))
        temporal_vec = (backbone_out).reshape(B, self.sequence_size//3, -1)
        return self.TA(temporal_vec)