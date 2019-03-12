# DHCP Starvation Lab
![](https://img.shields.io/badge/license-Apache--2.0-brightgreen.svg)

In this lab we will use [Kali](https://www.kali.org), [Ubuntu](https://www.ubuntu.com) & [Scapy](https://scapy.net/). 

## Lab Overview
***The Dynamic Host Configuration Protocol (DHCP)*** is a network management protocol used on UDP/IP networks whereby a DHCP server dynamically assigns an IP address and other network configuration parameters to each device on a network so they can communicate with other IP networks.

When a client system without an IP address enters a network it will request an IP address from the resident DHCP server. The DHCP server will reserve an IP address (so anyone else asking for one is not granted this one) and it will send that IP address to the device along with a lease identifying how long the address will be valid. Normally, from this point, the device will respond by confirming the IP address with the DHCP server and the DHCP server finally responds with an acknowledgement.

***The DHCP Starvation***, once the adversary receives the IP address and the lease period from the DHCP server, the adversary does not respond with the confirmation. Instead, the adversary floods the DHCP server with IP address requests until all addresses within the server’s address space have been reserved (exhausted). At this point, any hosts wishing to join the network will be denied access, resulting in a denial of service.

## Lab Environment
If [VirtualBox](https://www.virtualbox.org) is not installed on your computer, install it now.<br>

Path: `cd "C:\Program Files\Oracle\VirtualBox\"`<br>

- DHCP VM:<br>
  `VBoxManage startvm "Ubuntu"`<br>
- Victim VM:<br>
  `VBoxManage startvm "Ubuntu"`<br>
- Attacker VM:<br>
  `VBoxManage startvm "Kali"`<br>

![](Images/dhcp_spoofing.jpg)

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
