#!/usr/bin/env python3

import subprocess
import optparse

def shellcommand(text):
    subprocess.call(text, shell=True)

def change_mac(interface, mac):
    shellcommand('ifconfig ' + interface + ' down')
    shellcommand('ifconfig ' + interface + ' hw ether ' + mac)
    shellcommand('ifconfig ' + interface + ' up')
    print("\n\n[+] Changing MAC Address for " + interface + " to " + mac)
    print("\n done!")

def show_result():
    answ = str(input("\nwant to see results? (y/n): "))
    if answ == "":
        answ = "n"
        exit(0)
    elif answ == "y":
        shellcommand("ifconfig")
    elif answ == "n":
        print("\nByeee!")
        exit(0)
    else:
        print("Error")

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

options = get_arguments()
change_mac(options.interface, options.new_mac)
show_result()

# 34:45:56:67:78:89
