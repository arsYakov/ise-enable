import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import getpass
import easygui
from datetime import datetime
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ISE_IP = ""
ISE_SERVER = f"https://{ISE_IP}:9060/ers/config/"
HEADERS = {'Content-type':'application/json', 'Accept':'application/json'}
ISE_USER = ""

# Need to add your ID groups in here
staticIdendtityGroups = {
	"Blocked List" : "",
}

def move_ID(mac, idGroup, ticketID, description):
	try:
		mac = str(mac)
		if description == 0:
			description = ' '
		dateCreated = time.strftime("%Y/%m/%d")
		idGroupName = idGroup
		idGroupID = staticIdendtityGroups[idGroup]
		getURL = ISE_SERVER + "endpoint/name/" + mac

		print("Looking into " + mac)

		getRequest = requests.get(getURL, headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)

		if getRequest.status_code == 404:
			print("Endpoint not in database.. Adding now.")
			postURL = ISE_SERVER + "endpoint"
			postPayload = {"ERSEndPoint": {"mac":mac}}
			requests.post(postURL, data = json.dumps(postPayload), headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)

		getRequest = requests.get(getURL, headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
		getRequest = getRequest.json()

		macID = getRequest['ERSEndPoint']['id']

		putURL = ISE_SERVER + "endpoint/" + macID
		payload = {"ERSEndPoint": {'description': description, "groupId": idGroupID, "staticGroupAssignment":'true', "customAttributes":{"customAttributes":{"DateCreated": dateCreated,"Ticket": ticketID}}}}
		change = requests.put(putURL, data = json.dumps(payload), headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
		checkChange = requests.get(getURL, headers= HEADERS, auth=HTTPBasicAuth(ISE_USER, PASSWORD), verify=False)
		checkChange = checkChange.json()

		if checkChange['ERSEndPoint']['groupId'] == idGroupID:
			print(f'{mac} moved to {idGroupName}')
			return "Migrated"
		else:
			print(f'{mac} had a problem')
			return "Didn't Move"
	except:
		print(f'Failed at {mac}')
		return "Bad Request"


def main():
	# Prompt for file
	start=datetime.now()

	macList = pd.read_excel(easygui.fileopenbox())

	macList = macList.fillna(0)

	macList["Moved"] = macList.apply(lambda row: move_ID(row['MACAddress'], row["ID Group"], row['Ticket ID'], row['Description']), axis=1)

	currentTime = time.strftime("%m-%d-%Y-%H-%M")

	macList.to_excel(f"ID-Group-Cleanup-{currentTime}.xlsx", index=False)

if __name__ == '__main__':
	PASSWORD = getpass.getpass()
	main()
