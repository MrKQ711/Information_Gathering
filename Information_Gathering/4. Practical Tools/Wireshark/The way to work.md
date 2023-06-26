# Content

- [Content](#content)
  - [What is WireShark?](#what-is-wireshark)
  - [The way to work](#the-way-to-work)
  
## What is WireShark?

- Wireshark is a free and open-source network protocol analyzer. It is commonly used to troubleshoot network issues, perform network security analysis, and investigate network traffic. Wireshark allows you to capture and view the packets that are transmitted over a network, and it provides detailed information about each packet, including the protocol, source and destination IP addresses, and the contents of the packet payload. With Wireshark, you can analyze network traffic in real-time or from saved captures, filter traffic by various criteria, and generate reports on network activity.

## The way to work

- Wireshark captures packets using a technology called "packet sniffing". To capture packets, Wireshark uses a software called "packet capture library", such as WinPcap on Windows or libpcap on Linux and macOS.
- When you start Wireshark, the program will display a list of available network interfaces to capture packets from. You can choose the interface that you want to capture packets from.
- Once you have selected a network interface, Wireshark will start monitoring network traffic on that interface. Whenever a packet is sent or received on that interface, Wireshark will begin recording the details of that packet, including both the header and the content of the packet.
- After capturing packets, Wireshark will display them in a list. You can view detailed information about each packet, including the source and destination addresses, information about the protocols used, the length of the packet, and the contents of the packet.
- From there, you can use Wireshark's features to analyze the information collected from the packet, including filtering, tracking, and analyzing network streams. Through this analysis, you can learn about the operation of the network, troubleshoot connectivity issues, identify security issues, and more.




