import subprocess
import re
import requests
import json
import os

url = 'http://api.mylnikov.org/geolocation/wifi?bssid='

def get_average_location():
    raw_text = subprocess.check_output("netsh wlan show all")
    decoded_text = raw_text.decode('utf-8', 'replace')
    BSSIDs = re.findall(r'\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}', decoded_text)[2:] # 1 is your mac, 2> are BSSIDs of APs
    points = 0
    lat = 0
    lon = 0
    for BSSID in BSSIDs:
        r = requests.get(url+BSSID)
        response = r.text
        json_response = json.loads(response)
        if(json_response['result'] != 200):
            continue
        points += 1
        # print(json_response)
        lat += json_response['data']['lat']
        lon += json_response['data']['lon']
    if points == 0:
        raise ValueError('There are no AP nearby!')
    return str(lat / points) + ',' + str(lon / points)



def get_location():
    raw_text = subprocess.check_output("netsh wlan show interfaces")
    decoded_text = raw_text.decode('utf-8', 'replace')
    macs = re.findall(r'\S{2}:\S{2}:\S{2}:\S{2}:\S{2}:\S{2}', decoded_text)
    BSSID = macs[1] # 2 is BSSID of conected AP

    r = requests.get(url+BSSID)
    response = r.text
    json_response = json.loads(response)
    if(json_response['result'] != 200):
        raise ValueError('There are no AP nearby!')
    lat = json_response['data']['lat']
    lon = json_response['data']['lon']
    return str(lat) + ',' + str(lon)


def main():
    result = get_location()
    os.system("start chrome https://www.google.nl/maps/place/%s"%result)

    result = get_average_location()
    os.system("start chrome https://www.google.nl/maps/place/%s"%result)


if __name__ == '__main__':
    main()
    