import os, json

def event_loading(path: str) -> list:
    dataset = []

    if not os.path.isdir(path):
        raise FileNotFoundError(f'Path does not exists: {path}')

    for jfile in [f"{path}/{file}" for file in os.listdir(path) if file[-4:] == 'json']:
        with open(jfile) as f:
            dataset += json.load(f)

    return dataset

def event_reduction(event: list, instruction) -> list:
    return instruction(event)