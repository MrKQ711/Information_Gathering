# Content

- [Content](#content)
  - [What is Netcat?](#what-is-netcat)
  - [The way to work](#the-way-to-work)
  
## What is Netcat?

- Netcat is a versatile networking utility that can be used to read from and write to network connections using TCP or UDP protocols. It allows users to create TCP/UDP connections, listen for incoming connections, transfer data between systems, perform port scanning, and much more. Netcat is often referred to as the "Swiss Army knife of networking tools" because of its flexibility and numerous use cases. It is available on most Unix-like operating systems and also has ports to Windows and other platforms.
- Different between UDP and TCP:
  - TCP (Transmission Control Protocol): is a reliable protocol that ensures data is sent to its destination without errors or data loss. It uses error control, validation, and synchronization mechanisms to ensure that the data is successfully transferred.
  - UDP (User Datagram Protocol): is an unreliable protocol that does not guarantee that data is sent to the destination. It does not use error control, validation, and synchronization mechanisms to ensure that the data is successfully transferred.
- One of the important features of TCP is the error checking mechanism. TCP uses a method called "acknowledgment" to ensure that data packets have been received successfully. If the acknowledgment status is not acknowledged, TCP will automatically resend the lost data packets. This helps to ensure that the data is transmitted to the destination correctly and completely.
- Furthermore, TCP also uses synchronization and flow control mechanisms to ensure that data is transmitted efficiently and without getting stuck in transit.

## The way to work

- When Netcat establishes a connection between two computers, it creates a socket (virtual drive) to allow the computers to transfer data to each other over the established connection.

- Socket is a communication mechanism between processes in the network. It allows processes to transmit and receive data with each other over the network. Sockets can be used with a variety of protocols, including TCP, UDP, and SCTP.
For example, when you use Netcat on computer A to send data to computer B, Netcat will create a socket on computer A and a socket on computer B. The socket on computer A is assigned the number 1, and socket on computer B is assigned number 2.

- When you enter data into Netcat on computer A, Netcat will send this data through socket 1 to socket 2 on computer B. Socket 2 on computer B will receive this data and send a response back (if yes) for socket number 1 on computer A.


