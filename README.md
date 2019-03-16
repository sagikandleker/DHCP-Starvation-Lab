# DHCP Starvation Lab
![](https://img.shields.io/badge/license-Apache--2.0-brightgreen.svg)

In this lab we will use [Kali](https://www.kali.org), [Ubuntu](https://www.ubuntu.com) & [Scapy](https://scapy.net/). 

## Lab Overview
**The Dynamic Host Configuration Protocol (DHCP)** is a network management protocol used on UDP/IP networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network so they can communicate with other IP networks.

When a client system without an IP address enters a network it will request an IP address from the resident DHCP server. The DHCP server will reserve an IP address (so anyone else asking for one is not granted this one) and it will send that IP address to the device along with a lease identifying how long the address will be valid. Normally, from this point, the device will respond by confirming the IP address with the DHCP server and the DHCP server finally responds with an acknowledgement.

**The DHCP Starvation**, once the adversary receives the IP address and the lease period from the DHCP server, the adversary does not respond with the confirmation. Instead, the adversary floods the DHCP server with IP address requests until all addresses within the server’s address space have been reserved (exhausted). At this point, any hosts wishing to join the network will be denied access, resulting in a denial of service.

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

### Updating package tree in Ubuntu
In order to install an isc-dhcp-server in Kali Linux.<br>
First, we need to make sure the package tree is up –to-date with the latest software versions by issuing the below command.<br>
```sh
$ sudo apt-get update
```

### Installing DHCP Server in Ubuntu
Run the command below to install the DCHP server package, which was formerly known as dhcp3-server.<br>
```sh
$ sudo apt install isc-dhcp-server
```

When the installation completes, edit the file `/etc/default/isc-dhcp-server` to define the interfaces DHCPD should use to serve DHCP requests, with the INTERFACES option.<br>
For example, if you want the DHCPD daemon to listen on eth0, set it:<br>
```
INTERFACES="eth0"
```

### Configuring DHCP Server in Ubuntu
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
$ sudo systemctl start isc-dhcp-server.service
$ sudo systemctl enable isc-dhcp-server.service
```

### Configuring DHCP Client Machines
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

Save the file and exit. And restart network services like so (or reboot the system):<br>
```sh
$ sudo systemctl restart networking
```

## Lab Tasks
### Task 1: Run `run_script`.
**Describe what do you see on Sniff's screen?**

### Task 2: Improve `run_script`.


## Finish up
### Stop VM's
Run `VBoxManage startvm <vm_name>`, for example `VBoxManage startvm "Ubuntu"`

## Submission
You need to submit a detailed lab report, with screenshots, to describe what you have done and what you have observed.<br>
You also need to provide explanation to the observations that are interesting or surprising.<br>
Please also list the important code snippets followed by explanation.<br>
Simply attaching code without any explanation will not receive credits.
