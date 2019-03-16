from scapy.all import *

def main():
	broadcast = "ff:ff:ff:ff:ff:ff"
	conf.checkIPaddr = False
	ip_address_subnet = "10.0.0.120"
	subnet_mask = "255.255.255.0"
	dhcp_ip_address = "10.0.0.50"

	bogus_mac_address = RandMAC()
	dhcp_request = Ether(src=bogus_mac_address, dst=broadcast)/IP(src="0.0.0.0", dst=subnet_mask)/UDP(sport=68, dport=67)/BOOTP(chaddr=bogus_mac_address)/DHCP(options=[("message-type","request"),("server_id",dhcp_ip_address),("requested_addr", ip_address_subnet),"end"])

	sendp(dhcp_request)
	print "Requesting: " + ip_address_subnet + "\n"

if __name__=="__main__":
    main()
