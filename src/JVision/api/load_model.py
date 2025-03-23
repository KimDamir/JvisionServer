import torch
from dtrocr.model import DTrOCRLMHeadModel
from dtrocr.config import DTrOCRConfig

def load_model():
    model = DTrOCRLMHeadModel(DTrOCRConfig())
    model = torch.compile(model)
    model.load_state_dict(torch.load(f'api/model/Version2.pt'))
    model.eval()
    return model