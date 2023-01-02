#!/usr/bin/env python3

import subprocess
import optparse
import re

def shellcommand(text):
    subprocess.call(text, shell=True)

def change_mac(interface, mac):
    shellcommand('ifconfig ' + interface + ' down')
    shellcommand('ifconfig ' + interface + ' hw ether ' + mac)
    shellcommand('ifconfig ' + interface + ' up')
    print("\n[+] Changing MAC Address for " + interface)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change its MAC Address")
    parser.add_option("-m", "--mac", dest="new_mac", help="what MAC do you want to change")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("\n\n[-] Please specify an interface, use --help for more info!")
    elif not options.new_mac:
        parser.error("\n\n[-] Please specify a Mac Address, use --help for more info!")
    return options

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(['ifconfig',interface])
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("\n[-] Could not read Mac Address")

options = get_arguments()
current_mac = get_current_mac(options.interface)

print("\nCurrent MAC: "+str(current_mac))
if not current_mac: 
    exit(0)

change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)

if current_mac == options.new_mac:
    print("\n[+] MAC Address has successfully changed to: " + current_mac)
else:
    print("\n[-] MAC Address did not changed. ")

# 34:45:56:67:78:89
