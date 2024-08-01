import pandas as pd
from netmiko import Netmiko
from netmiko import ConnectHandler
from pandas import DataFrame
from datetime import datetime
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import concurrent.futures
import easygui
import getpass
import time
import requests
import json


# These variables are used for ISE API Calls
ISE_IP = ""
ISE_URL = f"https://{ISE_IP}:9060/ers/config/"
HEADERS = {'Content-type':'application/json', 'Accept':'application/json'}
ISE_USER = ""
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


"""

*******************************************
********* ISE REST API Section: ***********
*******************************************

"""


# Change_to_Enforcement
# This is used to move a switch from Learning to Enforcement Mode

def change_to_enforcement(switchip):
    try:
        getURL = ISE_URL + "networkdevice?filter=ipaddress.EQ." + switchip

        checkRecord = requests.get(getURL, headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
        checkRecord = checkRecord.json()
        switchID = checkRecord['SearchResult']['resources'][0]['id']

        idURL = ISE_URL + "networkdevice/" + switchID

        nadDetails = requests.get(idURL, headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
        nadDetails = nadDetails.json()

        try:
            isLearnModeIndex = nadDetails['NetworkDevice']['NetworkDeviceGroupList'].index('Device Type#All Device Types#Learn Mode')
            isLearnMode = nadDetails['NetworkDevice']['NetworkDeviceGroupList'][isLearnModeIndex]
            enforcementMode = 'Device Type#All Device Types#Enforcement Mode'
            nadDetails['NetworkDevice']['NetworkDeviceGroupList'][isLearnModeIndex] = enforcementMode
            changeMode = requests.put(idURL, json= nadDetails, headers = HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
            if changeMode.status_code == 200:
                print(f"{switchip} is moved")
                return "Moved to Enforcement Mode"
            else:
                print(f"{switchip} did not get moved")
                print(f'{changeMode.json}')
                return "Failed"
        except:
            print(f'{switchip} already in Enforcement Mode')
            return "Already in Enforcement Mode"
    except:
        print(f'Couldn\'t find {switchip} in ISE NAD description')
        return "Could not be found in ISE"


def main():
    start=datetime.now()

    print("Beginning Enforcement Script")

    print("Please Specify the list of switches to Enforce")

    time.sleep(1)

    enforceList = pd.read_excel(easygui.fileopenbox())

    print("Beginning Migration")

    enforceList['Status'] = enforceList.apply(lambda row: change_to_enforcement(row['Switch_IP']), axis = 1)

    currentTime = time.strftime("%m-%d-%Y-%H-%M")

    enforceList.to_excel(f"Enforce-Result-{currentTime}.xlsx", index=False)

    print(datetime.now()-start)

if __name__ == "__main__":
    PASSWORD = getpass.getpass()
    main()
