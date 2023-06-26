# Content

- [Content](#content)
  - [What is Tcpdump?](#what-is-tcpdump)
  - [The way to work](#the-way-to-work)
  
## What is Tcpdump?

- Tcpdump is a powerful command-line network sniffer tool for Linux/Unix systems that allows you to capture packets flowing through your network interface. It can display detailed information about each packet, such as its source and destination IP addresses, port numbers, protocol type, and packet size. Tcpdump is widely used by system administrators and network engineers for troubleshooting network issues and analyzing network traffic. It has various options and filters that allow you to customize the way it captures and displays packets.

## The way to work

- Tcpdump works using the functions provided by the packet capture library on the system. When started, tcpdump uses sockets to bind to a specific network interface and starts listening for packets that come through. 
- Tcpdump then uses filters to filter out the required packets. Filters can be used to limit the number of packets displayed by specifying criteria such as the IP address and destination or source port.
- After tcpdump has captured packets that match the filter, it displays detailed information about these packets. This information may include the IP addresses of the sender and receiver, the source and destination ports, the protocol type, and the content of the packet.
- All this information is displayed on the screen or can be saved to a file for later analysis.