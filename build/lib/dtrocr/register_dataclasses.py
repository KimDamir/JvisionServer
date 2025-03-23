import torch
from data import DTrOCRModelOutput, DTrOCRLMHeadModelOutput, DTrOCRProcessorOutput


def register_dataclasses():
    torch.export.register_dataclass(DTrOCRLMHeadModelOutput)
    torch.export.register_dataclass(DTrOCRModelOutput)
    torch.export.register_dataclass(DTrOCRProcessorOutput)
    print("Dataclasses registered.")