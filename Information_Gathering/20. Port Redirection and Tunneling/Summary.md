# Content

- [Content](#content)
  - [Port Forwarding](#port-forwarding)
    - [RINETD](#rinetd)
      - [The way to work](#the-way-to-work)
      - [Demo](#demo)
  - [SSH Tunneling](#ssh-tunneling)
    - [SSH Local Port Forwarding](#ssh-local-port-forwarding)
      - [Senorio](#senorio)
    - [SSH Remote Port Forwarding](#ssh-remote-port-forwarding)
    - [SSH Dynamic Port Forwarding](#ssh-dynamic-port-forwarding)
  - [PLINK.exe](#plinkexe)
  - [NETSH](#netsh)
  - [HTTPTunnel-ing Through Deep Packet Inspection](#httptunnel-ing-through-deep-packet-inspection)

  
## Port Forwarding
### RINETD

#### The way to work

- RINETD works on the principle of network packet delivery. When a network packet is sent from a client to a port on the server, RINETD receives the first packet and changes the destination information of this packet. Instead of sending the packet to the original port on the server, RINETD forwards (redirects) the packet to a different IP address and port that you previously configured.
- The working mechanism of RINETD includes the following steps.
  - Network packets are sent from the client to the server.
  - RINETD receives the first packet and checks the configuration rules.
  - If there is a corresponding configuration rule, RINETD changes the packet's destination information to forward it to the IP address and port specified in the rule.
  - The packet is then forwarded to the new server.
  - The new server receives the packet and processes it as usual.
- Through the above mechanism, RINETD allows you to forward connections from one IP address and port to another IP address and port in the network. This can be useful in many situations, such as forwarding web traffic from a corporate server to an external server or forwarding SSH requests to an internal server.

#### Demo

- As configured, our Kali machine can access the Internet, and the client can not. We can validate 
connectivity from our Kali machine by pinging google.com and connecting to that IP.
  ```bash
  ping google.com -c 1
  nc -nvv 172.217.27.46 80
  ```  
  ![Picture](../20.%20Port%20Redirection%20and%20Tunneling/Image/1.png)
- Next, we will SSH to the compromised Linux client and test Internet connectivity from there, again with Netcat.
  ```bash
  ssh thainguyen@172.29.37.55
  ```
  ![Picture](../20.%20Port%20Redirection%20and%20Tunneling/Image/2.png)
- We will use a port forwarding tool called rinetd590 to redirect traffic on our Kali Linux 
server. This tool is easy to configure, available in the Kali Linux repositories.
- The rinetd configuration file, ```bash /etc/rinetd.conf ```, lists forwarding rules that require four parameters, including bindaddress and bindport, which define the bound (“listening”) IP address and port, and connectaddress and connectport, which define the traffic’s destination address and port.
  ```bash
  cat /etc/rinetd.conf
  ```
  ![Picture](../20.%20Port%20Redirection%20and%20Tunneling/Image/3.png)
- This rule states that all traffic received on port 80 of our Kali Linux server, listening on all interfaces (0.0.0.0), regardless of destination address, will be redirected to google.com.
- This is exactly what we want. We can restart the rinetd service with service and confirm that the service is listening on TCP port 80 with ss (socket statistics).
  ```bash
  sudo service rinetd restart
  ss -antp | grep "80"
  ```
  ![Picture](../20.%20Port%20Redirection%20and%20Tunneling/Image/4.png)
- Excellent! The port is listening. For verification, we can connect to port 80 on our Kali Linux virtual machine.
  ![Picture](../20.%20Port%20Redirection%20and%20Tunneling/Image/5.png)

## SSH Tunneling
### SSH Local Port Forwarding

#### Senorio

- The situation is that you have successfully infiltrated a Linux machine through a remote vulnerability, gained special privileges to root and obtained credentials for the root and student users on that machine. This compromised Linux machine doesn't have any outbound communication restrictions and only opens the SSH port (port 22), RDP (port 3389) and the vulnerable service port, which are also allowed through the firewall.
- After listing the information on the compromised Linux machine, you discover that the machine has a different network interface connected to a different network (192.168.1.x). In this intranet subnet, you identify a Windows Server 2016 machine that has an available network share.
- In this situation, you want to interact with the new target machine from your Kali attack machine through the compromised Linux machine. This gives you access to all the tools on the Kali attack machine when interacting with the target machine.

### SSH Remote Port Forwarding
### SSH Dynamic Port Forwarding
## PLINK.exe
## NETSH
## HTTPTunnel-ing Through Deep Packet Inspection