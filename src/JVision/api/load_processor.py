from dtrocr.processor import DTrOCRProcessor
from dtrocr.config import DTrOCRConfig

def load_processor():
    test_processor = DTrOCRProcessor(DTrOCRConfig())
    return test_processor