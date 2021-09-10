import json
from os.path import dirname, abspath, join

root = dirname(dirname(abspath(__file__)))
with open(join(root, 'settings.json')) as f:
    settings = json.load(f)

