# Content

- [Content](#content)
  - [Display the filter and folloing the TCP Streams of FTP server](#display-the-filter-and-folloing-the-tcp-streams-of-ftp-server)
  - [Try with netcat](#try-with-netcat)
  
## Display the filter and folloing the TCP Streams of FTP server

- First, i start to wireshark in Kali and capture the local network.
- Then, i try to log in to the FTP anonymous server.
  ![FTP](../Wireshark/Image/1.png)
  ![FTP](../Wireshark/Image/2.png)
- Then, i filter to traffic in wire shark by using the filter `ftp` and or tcp.port == 21 (port 21 is the port of FTP)
  ![FTP](../Wireshark/Image/3.png)
- Finally, i open TCP Stream to see the traffic of FTP.
  ![FTP](../Wireshark/Image/4.png)

## Try with netcat

- In Windows, i open cmd and type `ncat -nlvp 4444` to create a chat between 2 computer. 
  ![FTP](../Wireshark/Image/5.png)
- In Kali, i type command `nc -nv 192.168.50.10 4444` to connect to the chat. I use wire shark to capture the traffic of this chat.
  ![FTP](../Wireshark/Image/6.png)
- I filter the traffic by using the filter `tcp.port == 4444` and open TCP Stream to see the traffic of this chat. (Port 443 is the port of HTTPS)
  ![FTP](../Wireshark/Image/7.png)
  ![FTP](../Wireshark/Image/8.png)

