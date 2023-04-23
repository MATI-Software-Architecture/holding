import xmltodict
import subprocess
import importlib
import json

def install(package: str):
    """
    Install a package using pip if it is not already installed
    """
    try:
        importlib.import_module(package)
    except ImportError:
        subprocess.check_call(['pip', 'install', package])


def convert(file: str, format: str, program: str) -> dict:
    """
    Convert a file into a dictionary
    """
    if format == 'json':
        data = json.loads(file)
    elif format == 'xml':
        data = xmltodict.parse(file)
    else:
        loc = {'data': {}, 'file': file}
        exec(program, globals(), loc)
        data = loc['data']
    return data


def flatten(data: dict) -> dict:
    """
    Flatten a nested dictionary
    """
    def _flatten(data: dict, prefix: str = '') -> dict:
        result = {}
        for key, value in data.items():
            if isinstance(value, dict):
                # result.update(_flatten(value, prefix + key + '.'))
                result.update(_flatten(value, key))
            else:
                # result[prefix + key] = value
                result[key] = value
        return result
    return _flatten(data)

