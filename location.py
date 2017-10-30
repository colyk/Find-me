import subprocess
import re
import requests
import json
import os

def get_average_location():
    url = 'http://api.mylnikov.org/geolocation/wifi?bssid='

    raw_text = subprocess.check_output("netsh wlan show all")
    decoded_text = raw_text.decode('utf-8', 'replace')
    BSSIDs = re.findall(r'\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}', decoded_text)[2:] # 1 is your mac, 2 is BSSID of connected wifi
    k = 0
    lat = 0
    lon = 0
    for BSSID in BSSIDs:
        r = requests.get(url+BSSID)
        response = r.text
        json_response = json.loads(response)
        if(json_response['result'] == 404):
            continue
        k += 1
        # print(json_response)
        lat += json_response['data']['lat']
        lon += json_response['data']['lon']
    return str(lat/k)+','+str(lon/k)



def get_location():
    url = 'http://api.mylnikov.org/geolocation/wifi?bssid='

    raw_text = subprocess.check_output("netsh wlan show interfaces")
    decoded_text = raw_text.decode('utf-8', 'replace')
    macs = re.findall(r'\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}', decoded_text)
    BSSID = macs[1]

    r = requests.get(url+BSSID)
    response = r.text
    json_response = json.loads(response)
    if(json_response['result'] == 404):
        return None
    lat = json_response['data']['lat']
    lon = json_response['data']['lon']
    return str(lat)+','+str(lon)


def main():
    result = get_location()
    os.system("start chrome https://www.google.nl/maps/place/%s"%result)

    result = get_average_location()
    os.system("start chrome https://www.google.nl/maps/place/%s"%result)


if __name__ == '__main__':
    main()