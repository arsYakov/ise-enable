# Enable ISE Scripts

These scripts are to migrate a list of switches and endpoints into ISE enable mode. 

The terminology used here is "Learn Mode" and "Enforcement Mode"

The switch migration switches each switch in the provided template file into the network device group within ISE, which will begin offering restricted access to endpoint that do not authenticate properly on said switch.

The endpoint migration script is used to whitelist several endpoints at once. The provided template file can be used to drop them into the specific identiy group needed prior to enforcement of the switch. 
