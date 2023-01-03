#!/usr/bin/env python3

# for this, we will use de module scapy that allow us to 
# work with the ARP protocol
import scapy.all as scapy
import optparse as opt

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc }
        clients_list.append(client_dict)

    return clients_list

def print_result(results_list):
    print("IP\t\t\tMAC Address\n---------------------------------------")
    for client in results_list:
        print(f"{client['ip']}\t\t{client['mac']}")

def get_arguments():
    parser = opt.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Define what target, or range of targets would like to discover!")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please, specify what target or range of targets you are looking for!")
    return options

options = get_arguments()
print_result(scan(options.target))