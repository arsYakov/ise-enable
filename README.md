# Enable ISE Scripts

These scripts are to migrate a list of switches and endpoints into ISE enable mode. 

The terminology used here is "Learn Mode" and "Enforcement Mode"

The switch migration moves each switch in the provided template file into the desired network device group within ISE which will begin offering restricted access to endpoint that do not authenticate properly on said switch.

The endpoint migration script is used to whitelist several endpoints at once. The provided template file can be used to drop them into the specific identiy group needed prior to enforcement of the switch, and add any custom attributes such as ticket ID for business tracking. 
