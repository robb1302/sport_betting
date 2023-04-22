import torch.nn as nn
import torch


class PrecisionLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, output, target):
        if len(output.shape)>1:
            output = output[:,1]

        output = torch.clamp(output,0,1)>0.5
        target = torch.clamp(target,0,1)>0.5
        # loss = torch.sum(torch.abs(self.X_train_subset) * (torch.abs(target)-torch.abs(output)))/ torch.sum(torch.abs(self.X_train_subset))
        precision = torch.sum((target == True) & (output == True))/(torch.sum( output == True)+1)
        loss = 1-precision
        
        return loss