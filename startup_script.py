from scapy.all import ARP, Ether, srp
import os
import time

self_ip = "192.168.0.101" # bound ip address of self
target_ip = "192.168.0.1/24" #"192.168.1.1/24"
router_ip = "192.168.0.1"
try:
    while True:

        # IP Address for the destination
        # create ARP packet
        arp = ARP(pdst=target_ip)
        # create the Ether broadcast packet
        # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        # stack them
        packet = ether/arp

        result = srp(packet, timeout=3, verbose=0)[0]

        # a list of clients, we will fill this in the upcoming loop
        clients = []

        # a list of the ip addresses connected to the network
        ip_addresses = []

        for sent, received in result:
            # for each response, append ip and mac address to `clients` list
            # ip address : received.psrc
            clients.append({'ip': received.psrc, 'mac': received.hwsrc})
            ip_addresses.append(received.psrc)

        for ip_address in ip_addresses:
            if (ip_address != self_ip and ip_address != router_ip):
                print("Trying to open server with client ip address: " + ip_address)
                command_string = "python3 /home/pi/Desktop/netgear_server.py " + ip_address + " 8080"
                print(command_string)
                os.system(command_string)
        print("scan done, looping again")
        clients.clear()
        ip_addresses.clear()
        time.sleep(1)
except KeyboardInterrupt:
    print('interrupted!')
