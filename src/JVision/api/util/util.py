from dtrocr.processor import DTrOCRProcessor
from dtrocr.config import DTrOCRConfig

def create_processor():
    processor = DTrOCRProcessor(DTrOCRConfig())
    return processor