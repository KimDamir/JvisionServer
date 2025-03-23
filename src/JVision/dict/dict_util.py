import json

def save_dict(dict, output_dir):
    with open(str(output_dir / 'labels.json'), 'w') as fp:
        json.dump(dict, fp)
        
def load_dict(path):
    with open(str(path / 'images' / 'labels.json'), 'r') as fp:
        data_dict = json.load(fp)
    return data_dict