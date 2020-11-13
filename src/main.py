import json
import subprocess
from typing import Dict, List

ssid_pswd_mapping: Dict[str, str] = {}
wifi_profiles: str = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode()
ssid_names: List[str] = [line.split(':')[1].strip() for line in wifi_profiles.split('\n') if 'All User Profile' in line]

for ssid in ssid_names:
    psdw_output: str = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear']).decode()
    pswds: List[str] = [line.split(':')[1].strip() for line in psdw_output.split('\n') if 'Key Content' in line]
    try:
        ssid_pswd_mapping[ssid] = pswds[0]
    except IndexError:
        continue

with open('./passwords.json', 'w') as f:
    f.write(json.dumps(ssid_pswd_mapping))
