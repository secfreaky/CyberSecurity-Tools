import subprocess
import optparse
import time
import re
import sys
from colorama import Fore,Style

macspoofer = Fore.YELLOW +  """
 _______  _______  _______  _______  _______  _______  _______  _______  _______  _______ 
(       )(  ___  )(  ____ \(  ____ \(  ____ )(  ___  )(  ___  )(  ____ \(  ____ \(  ____ )
| () () || (   ) || (    \/| (    \/| (    )|| (   ) || (   ) || (    \/| (    \/| (    )|
| || || || (___) || |      | (_____ | (____)|| |   | || |   | || (__    | (__    | (____)|
| |(_)| ||  ___  || |      (_____  )|  _____)| |   | || |   | ||  __)   |  __)   |     __)
| |   | || (   ) || |            ) || (      | |   | || |   | || (      | (      | (\ (   
| )   ( || )   ( || (____/\/\____) || )      | (___) || (___) || )      | (____/\| ) \ \__
|/     \||/     \|(_______/\_______)|/       (_______)(_______)|/       (_______/|/   \__/
"""
print(macspoofer)
print(Fore.WHITE + "Made by Secfreaky with Love <3!")

def is_sudo():
    try:
        subprocess.check_output(["sudo", "-n", "ls"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        return False
def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i" , "--interface" , dest ="interface" , help="Interface to change its  MAC Address")
	parser.add_option("-m", "--mac" , dest = "spoofed_mac" , help = "New Mac Address")
	(options,arguments) = parser.parse_args()
	if not options.interface:
		parser.error(Fore.RED + "[-] Please specify the interface properly\n")
	elif not options.spoofed_mac:
		parser.error(Fore.RED + "[-] Please specify the New MAC Properly\n")
	return options

def final_check(interface,spoofed_mac):
	card_info = subprocess.check_output(["ifconfig",interface]).decode("ascii")
	current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",card_info)
	if(current_mac.group(0) == spoofed_mac):
		print(Fore.BLUE + "[+] MAC Address Spoofed Successfully , Happy Hacking!\n")
	else:
		print(Fore.RED + "[-] Enter new MAC Address Properly!\n")
	return current_mac.group(0)

def adapter_info(interface):
	time.sleep(2)
	print(Fore.BLUE + "[+] Have a look at your mac <3!\n")
	time.sleep(2)
	subprocess.call(["ifconfig" , interface])

def spoof_mac(interface,spoofed_mac):
	print(Fore.BLUE + "\n[+] Spoofing MAC address for "+interface+" to "+ spoofed_mac +"\n")
	subprocess.call(["ifconfig" , interface , "down"])
	subprocess.call(["ifconfig" , interface , "hw" , "ether" , spoofed_mac])
	subprocess.call(["ifconfig" , interface , "up"])

options = get_arguments()
if is_sudo():
	spoof_mac(options.interface,options.spoofed_mac)
else:
	print(Fore.RED + "[-] You are not a root user , use sudo su for root privileges.")
	sys.exit()	
time.sleep(2)
if(final_check(options.interface,options.spoofed_mac) == options.spoofed_mac):
	time.sleep(2)
	adapter_info(options.interface)
