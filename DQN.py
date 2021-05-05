import torch.nn as nn

class DQN(nn.Module):
  def __init__(self):
    super(DQN, self).__init__()
    self.input_layer = nn.Sequential(nn.Linear(4, 64), nn.ReLU(inplace=True))
    self.middle_layer = nn.Sequential(nn.Linear(64,64), nn.ReLU(inplace=True))
    self.output_layer = nn.Sequential(nn.Linear(64, 1))

    self.init_weights()

  def init_weights(self):
    for m in self.modules():
      if type(m) == nn.Linear:
          nn.init.xavier_uniform_(m.weight)
          nn.init.constant_(m.bias, 0)

  def forward(self, x):
    x = self.input_layer(x)
    x = self.middle_layer(x)
    x = self.output_layer(x)
    return x