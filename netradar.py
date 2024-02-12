import scapy.all as scapy
import argparse
import netifaces
import subprocess
import time
import sys
from colorama import Fore,Style

ascii_art = Fore.LIGHTYELLOW_EX + r"""
 _        _________________ _______  _______  ______   _______  _______
( (    /|(  ____ \__   __/(  ____ )(  ___  )(  __  \ (  ___  )(  ____ )
|  \  ( || (    \/   ) (   | (    )|| (   ) || (  \  )| (   ) || (    )|
|   \ | || (__       | |   | (____)|| (___) || |   ) || (___) || (____)|
| (\ \) ||  __)      | |   |     __)|  ___  || |   | ||  ___  ||     __)
| | \   || (         | |   | (\ (   | (   ) || |   ) || (   ) || (\ (   
| )  \  || (____/\   | |   | ) \ \__| )   ( || (__/  )| )   ( || ) \ \__
|/    )_)(_______/   )_(   |/   \__/|/     \|(______/ |/     \||/   \__/
"""
print(ascii_art)
print(Fore.WHITE + "Made by Secfreaky with Love <3!\n")
def is_sudo():
    try:
        subprocess.check_output(["sudo", "-n", "ls"], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        return False

def get_gateway_ip():
    try:
        gateway_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
        return gateway_ip + "/24"
    except Exception as e:
        return str(e)

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    options = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(results_list):
    print(Fore.RED + "IP Address\tMAC Address")
    print(Fore.YELLOW + "-----------------------------------------")
    for client in results_list:
        time.sleep(1)
        print(Fore.BLUE + client["ip"] + "\t" + client["mac"])

def exit_message():
    print(Fore.LIGHTBLACK_EX + "\n[-] Goodbye! Thank You For Using our Tools <3!")



try:
    options = get_arguments()
    if(is_sudo()):
        scan_result = scan(get_gateway_ip())
        print_result(scan_result)
        pass
    else:
        print(Fore.RED + '[-] You require root permissions to run this tool!')
except KeyboardInterrupt:
    exit_message()
    sys.exit(0)
