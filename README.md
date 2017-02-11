This tool automates the discovery of "allowElevate"==True in exe file manifests. It's usually used in privilege escalation scenarios.

For more detailed info read:  [Bypassing Windows User Account Control (UAC) and ways of mitigation](https://www.greyhathacker.net/?p=796) 

    
### Requirements
-----------------------------
* python 2.7.x
* pefile
* tabulate 
* BeautifulSoup

    
### Compatibility
-----------------------------
* MS Windows
	
	
### Usage
-----------------------------
usage: elevate_check.py [-h] [-d DIRECTORY] [-r] [-i]

optional arguments:
  -h, show this help message and exit
  
  -d DIRECTORY      Target directory.
  
  -r&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Scan subfolders as fell.
  
  -i&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ignore files manufactured by Microsoft.

### Output
----------------------------
![Expected output](allowElevate.png?raw=true "Expected output")
