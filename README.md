## Powershell script Obfuscator
#### part of the convoluted python series...
![Screenie](https://github.com/loneferret/cheapObfuscator/blob/master/screenie.png)

#### Requirements
```
requests
https://pypi.python.org/pypi/requests/2.11.1
Install : pip install requests==2.11.1
```

```
usage: obfuscatePSH.py [-h] --psh PSHSCRIPT

Simple & Convoluted Powershell obfuscation tool  v0.1.1:
Grabs a Powershell script from the tubes, remplaces function names & calls
To randomly generated string, and removes block comments & empty lines etc.
	* Currently only changes function name.
	* Does variable names but could be better

Author: Steven McElrea (loneferret)
License: Apache License 2.0
Status: Prototype

You can experiment and try the script on some of these examples here:
http://www.robvanderwoude.com/powershellexamples.php

Example Usage:
	./obfuscatePSH.py --psh InveighRelay
	./obfuscatePSH.py -p Mimikatz

optional arguments:
  -h, --help            show this help message and exit
  --psh PSHSCRIPT, -p PSHSCRIPT
                        Available scripts to download:
                        - Mimikatz
                        - InveighRelay
			- Test [ Will prompt for a URL to fetch text ]

```
