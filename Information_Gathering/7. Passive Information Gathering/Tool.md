# Content

- [Content](#content)
  - [DNS Enumeration](#dns-enumeration)
    - [Interacting with a DNS Server](#interacting-with-a-dns-server)
      - [The way to work](#the-way-to-work)
      - [Demo](#demo)
    - [Forward Lookup Brute Force](#forward-lookup-brute-force)
    - [Relevant Tools in Kali Linux](#relevant-tools-in-kali-linux)
      - [DNSRecon](#dnsrecon)
        - [The way to work](#the-way-to-work-1)
        - [Demo](#demo-1)
  - [Port Scanning](#port-scanning)
    - [Port Scanning with Nmap](#port-scanning-with-nmap)
      - [The way to work](#the-way-to-work-2)
      - [Stealth / SYN Scanning](#stealth--syn-scanning)
        - [How it works](#how-it-works)
        - [Demo](#demo-2)
      - [TCP Connect Scanning](#tcp-connect-scanning)
        - [How it works](#how-it-works-1)
        - [Demo](#demo-3)
      - [UDP Scanning](#udp-scanning)
        - [The way to work](#the-way-to-work-3)
        - [Demo](#demo-4)
      - [Network Sweeping](#network-sweeping)
        - [The way to work](#the-way-to-work-4)
        - [Demo](#demo-5)
      - [OS Fingerprinting](#os-fingerprinting)
        - [The way to work](#the-way-to-work-5)
        - [Demo](#demo-6)
      - [Banner Grabbing/Service Enumeration](#banner-grabbingservice-enumeration)
      - [Nmap Scripting Engine (NSE)](#nmap-scripting-engine-nse)
        - [The way to work](#the-way-to-work-6)
        - [Demo](#demo-7)
    - [Masscan](#masscan)
      - [The way to work](#the-way-to-work-7)
  - [SMB Enumeration](#smb-enumeration)
    - [Nmap SMB NSE Scripts](#nmap-smb-nse-scripts)
      - [Demo](#demo-8)
  
## DNS Enumeration
### Interacting with a DNS Server

#### The way to work

- Host command works is to send a DNS query to the DNS server configured on your system (usually the DNS server provided by your carrier or ISP). This DNS server will check the DNS records associated with the requested domain name and return the results to your computer. When you make a DNS query for the first time for a domain name, DNS data must be downloaded from the DNS server, and then stored in the cache on your computer for faster access the next time for the next DNS query.
- When your DNS server has no information about the requested domain name, it will continue to query other DNS servers until it finds a DNS server that contains information about that domain. This process is called "recursive" and is done by the DNS server. That is, the DNS server will search from your nearest DNS server to other DNS servers further away until it finds a result.

#### Demo

 ![Picture](../7.%20Passive%20Information%20Gathering//Image/1.png)
- To demonstrate this, we’ll use the host command to find the IP address of 
www.epicnpc.com.
- We can use the -t option to specify the type of record we are 
looking for.

### Forward Lookup Brute Force

- We create a list of service names and then use the host command to query the DNS server for each service name. If the DNS server returns an IP address, we know that the service is running on the target system.
 ![Picture](../7.%20Passive%20Information%20Gathering/Image/2.png)

### Relevant Tools in Kali Linux
#### DNSRecon

##### The way to work

- When DNSRecon receives a domain name from a user, it makes DNS requests to look up the DNS records associated with that domain. To make DNS requests, DNSRecon uses the Python socket function to connect and communicate with the DNS server.
- When DNSRecon sends a DNS request to a DNS server, the request travels through networks and devices on its way from the user's computer to the DNS server. This request can be intercepted or spoofed in the event that the network or device in its path is hacked or compromised.
- Actually, the way to work of dnsrecon is similar to host command.
  
##### Demo

  ![Picture](../7.%20Passive%20Information%20Gathering/Image/3.png)
- The -t axfr option in DNSRecon will attempt to send a zone transfer request to the specified DNS server, if successful, DNSRecon will collect all DNS records of the domain name and enumerate them.

## Port Scanning
### Port Scanning with Nmap

#### The way to work

- Nmap is a network port scanning tool. When you provide an IP address to Nmap, it scans the ports on that address to determine which ports are open and active on that server. By default, Nmap will scan all ports from 0 to 65535, but you can specify a specific port range to scan using Nmap's options. After completing the scan, Nmap will display the scan results, showing which ports are active and detailed information about them, helping users assess the safety of the scanned network.
- When you use Nmap to scan an IP address, it creates a connection to each port on that server to check if the port is open. If the port is open, Nmap will receive a response from that server through the socket connection corresponding to that port.

#### Stealth / SYN Scanning 

##### How it works

- SYN scanning is a TCP port scanning method that involves sending SYN packets to various ports on a target machine without completing a TCP handshake. This means that if a TCP port is open, a SYN-ACK should be sent back from the target machine, informing the scanner that the port is open. At this point, the port scanner does not bother to send the final ACK to complete the three-way handshake, which makes the scan much faster and less conspicuous.
- Additionally, SYN scanning allows Nmap to avoid detection by certain types of intrusion detection systems (IDS) and firewalls that are configured to detect and block other types of scans. By using this stealthy scanning technique, Nmap can reduce its footprint and avoid detection while still providing valuable information about the target network or host.

##### Demo

  ![Picture](../7.%20Passive%20Information%20Gathering/Image/4.png)

#### TCP Connect Scanning

##### How it works

- The operation mechanism of TCP Connect Scan in Nmap includes the following steps:
  - Nmap makes a TCP connection to the destination port and looks at the response from the target. If the port is open, Nmap will receive a SYN/ACK response from the target.
  - After receiving the SYN/ACK response, Nmap sends an RST (Reset) request to close the established TCP connection.
  - If the port is closed or blocked by a firewall, Nmap will receive an RST response from the target and understand that the port is closed.
  - Depending on how the TCP connection is established, port scanning can take a long time. To minimize scanning time, Nmap allows the use of options such as -n to not perform DNS resolution or -Pn to skip checking for the existence of the target.

##### Demo

 ![Picture](../7.%20Passive%20Information%20Gathering/Image/5.png)

#### UDP Scanning

##### The way to work

- UDP Scanning is a method of scanning network ports in which the Nmap program uses UDP packets to send requests to ports on the destination host. When a UDP packet is sent to a port, the destination server will not send back any response if the port is closed or unlisted.
- Due to the nature of the UDP protocol, UDP port scanning will be more difficult than TCP Scanning because UDP packets will not have a handshake like in TCP Scanning. This increases the number of UDP packets that need to be sent and thus increases the scan time.
- During TCP scanning, it establishes a TCP connection with the port under test by performing a three-way handshake and determines if the server responds or not. Whereas, during UDP scanning, it just sends requests to a specific IP address and waits for a response from the server. However, due to the connectionless nature of the UDP protocol, determining if a certain port is open can be more difficult than TCP scanning. This is because the server may not respond to UDP requests or respond with an ambiguous packet, and thus determining the state of that port may become more difficult.

##### Demo

 ![Picture](../7.%20Passive%20Information%20Gathering/Image/6.png)
- (-sS) option to build a more complete picture of our target.
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/7.png)

#### Network Sweeping

##### The way to work

- Ping sweep is a technique used in scanning a network to determine which devices on the network are active by sending an ICMP Echo Request to each IP address on a subnet and waiting for a response. response from those devices.
- When a device receives an ICMP Echo Request, it sends back an ICMP Echo Reply for the source IP address of that request. If there is no response after sending an ICMP Echo Request, it may indicate that the device has gone down or may have been blocked by firewall filters.

##### Demo

  ![Picture](../7.%20Passive%20Information%20Gathering/Image/7.png)
- After that, we can use option -oG to save the result to a file.
  `nmap -v -sn 104.20.38.149-254 -oG ping-sweep.txt`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/8.png)
- Then i get all of ip i get. 
  `grep Up ping-sweep.txt | cut -d “ “ -f 2`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/9.png)
- We determine a specific port and try to scan it on all the IP addresses we have found.
  `nmap -p 80 104.20.38.149-254 -oG web-sweep.txt`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/10.png)
- The command "nmap -sT -A --top-ports=20 10.11.1.1-254 -oG top-port-sweep.txt" is used to scan multiple IP addresses in the range from 10.11.1.1 to 10.11.1.254 and checks the most common TCP ports, including the 20 ports identified by the "--top-ports" option.
- The "-sT" option is used to perform a TCP connect scan, i.e. opening connections to scanned ports to determine if they are active. The "-A" option is used to enable the server's OS version determination, script scanning, and traceroute calculation.
- When the scan is complete, the results will be saved to a text file called "top-port-sweep.txt". This is a more holistic approach to scan multiple computers in the same network and help detect security vulnerabilities and existence of services running on ports.
  `nmap -sT -A --top-ports=20 104.20.38.149-254 -oG top-port-sweep.txt`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/11.png)

#### OS Fingerprinting

##### The way to work

- OS Fingerprinting is an important function in Nmap that allows to determine the type of operating system (OS) running on a scanned computer by analyzing the responses from network packets.
- When performing an OS Fingerprinting scan in Nmap, Nmap sends a series of requests and looks at the computer's response to determine the operating system type. This process is based on differences in how the operating system responds to network requests, such as response times or TCP flag values set in the response.
- Nmap uses the OS database to compare the collected information and determine the corresponding operating system type. The results of the OS Fingerprinting function are useful for detecting already compromised systems or for detecting new devices connected to the network and determining what operating system they are running. The option used for this function is "-O" in the Nmap scan command.

##### Demo

 `nmap -O 104.20.38.149`
 ![Picture](../7.%20Passive%20Information%20Gathering/Image/12.png)

#### Banner Grabbing/Service Enumeration

- We can also identify services running on specific ports by inspecting service banners (-sV) and running various OS and service enumeration scripts (–A) against the target.
  `nmap -sV -sT -A 104.20.38.149`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/12.png)

#### Nmap Scripting Engine (NSE)

##### The way to work

- It refers to the Nmap Scripting Engine (NSE), a feature of Nmap that allows users to execute custom scripts to automate various scanning tasks. These scripts are written in the Lua language and are stored in the /usr/share/nmap/scripts directory.
- NSE scripts can be used to perform a variety of tasks, including DNS enumeration, brute force attacks, and vulnerability identification. Using NSE helps automate security testing and reduces the amount of manual work that needs to be done.

##### Demo

- The example use the smb-os-discovery script to determine the operating system running on a remote server. When Nmap runs with the "--script=smb-os-discovery" option, it executes this script and tries to connect to the SMB service on that server to determine its operating system.
  `nmap 104.20.38.149 -–script=smb-os-discovery`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/13.png)

### Masscan

#### The way to work

- Masscan is a port scanning tool developed for scanning computer networks and finding active devices on the network. Masscan's mechanism of action is to use the 4th layer TCP/IP scanning technique to send TCP or UDP packets to specified destination ports on one or more IP addresses. When Masscan receives responses from network devices, it analyzes and aggregates the information to generate a report on the open ports and services available on each device. Masscan is designed to work at very high speeds, allowing large networks to be scanned in a short amount of time.

## SMB Enumeration

- SMB enumeration is the process of finding useful information about the SMB (Server Message Block) system on a server or network. SMB is a protocol used to share resources, such as files and printers, between computers in a Windows network.
- The SMB enumeration process includes gathering information about SMB servers, finding shared files and folders on the system, and determining user access rights to files and folders. this part.

### Nmap SMB NSE Scripts

#### Demo

- Nmap contains many useful NSE scripts that can be used to discover and enumerate SMB 
services. These scripts can be found in the /usr/share/nmap/scripts directory.
  `ls -1 /usr/share/nmap/scripts/smb*` 
  `nmap -v -p 139, 445 --script=smb-os-discovery 104.20.38.149`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/14.png)
- To check for known SMB protocol vulnerabilities, we can invoke one of the smb-vuln NSE scripts. 
- We will take a look at smb-vuln-ms08-067, which uses the --script-args option to pass 
arguments to the NSE script.
  `nmap -v -p 139,445 --script=smb-vuln-ms08-067 --script-args=unsafe=1 104.20.38.149`
  ![Picture](../7.%20Passive%20Information%20Gathering/Image/15.png)
