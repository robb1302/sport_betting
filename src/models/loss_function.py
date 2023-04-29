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
        precision = torch.sum((target == True) & (output == True))/(torch.sum( output == True)+1)
        loss = 1-precision
        
        return loss
    

class TotalValueLoss(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, output, target):
        if len(output.shape)>1:
            output = output[:,1]

        output = torch.clamp(output,0,1)>0.5
        target = torch.clamp(target,0,1)>0.5
        right_picks = torch.sum((target == True) & (output == True))
        wrong_picks = torch.sum((target == False) & (output == True))
       
        loss = wrong_picks - right_picks
        
        return loss