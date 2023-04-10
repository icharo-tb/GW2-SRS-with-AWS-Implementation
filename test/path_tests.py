import os

print(os.path.basename('logger_test.py'))


import requests

res = requests.get('https://gw2wingman.nevermindcreations.de/logContent/20230305-224905_vg_kill',timeout=3)
print(res.status_code)