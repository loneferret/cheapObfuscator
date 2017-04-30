### Powershell script Obfuscator
![Screenie](https://github.com/loneferret/cheapObfuscator/blob/master/screenie.png)

```
usage: obfuscatePSH.py [-h] --psh PSHSCRIPT

Simple & Convoluted Powershell obfuscation tool  v0.1.1:
Grabs a Powershell script from Github, remplaces function names & calls
To randomly generated string, and removes block comments & empty lines.
	* Currently only changes function name.

Author: Steven McElrea (loneferret)
License: Apache License 2.0
Status: Prototype

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
