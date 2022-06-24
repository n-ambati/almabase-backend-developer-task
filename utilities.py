import json
from json.decoder import JSONDecodeError


def read_input():
    with open('data.json', 'r') as f:
        try:
            data = json.load(f)
            return data
        except JSONDecodeError:
            return None


def save(result):
    with open('result.json', 'w') as f:
        data = {'result': list(result)}
        json.dump(data, f)
