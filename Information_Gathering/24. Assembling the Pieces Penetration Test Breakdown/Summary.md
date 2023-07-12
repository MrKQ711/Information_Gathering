# Content

- [Content](#content)
  - [Targeting the Database](#targeting-the-database)
    - [Enumeration](#enumeration)
      - [Application/Service Enumeration](#applicationservice-enumeration)
    - [Attempting to Exploit the Database](#attempting-to-exploit-the-database)
      - [Why We Failed](#why-we-failed)
  - [Targeting Poultry](#targeting-poultry)
    - [Poultry Enumeration](#poultry-enumeration)
      - [Network Enumeration](#network-enumeration)
    - [Exploitation (Or Just Logging In)](#exploitation-or-just-logging-in)
    - [Poultry Post-Exploitation Enumeration](#poultry-post-exploitation-enumeration)
    - [Unquoted Search Path Exploitation](#unquoted-search-path-exploitation)
  - [Internal Network Enumeration](#internal-network-enumeration)
  - [Targeting the Jenkins Server](#targeting-the-jenkins-server)
    - [Application Enumeration](#application-enumeration)
    - [Exploiting Jenkins](#exploiting-jenkins)


## Targeting the Database
### Enumeration

- At this point in the enumeration step of the database, we already know a couple of things. Because of access to the WordPress server, we know that the host is in a different network than we are currently on. We also know that we are running MariaDB version 10.3.20. A quick Google search shows us this is a fairly new version. This presents a problem as a new version most likely won’t have vulnerabilities that lead to remote code execution.
- Let’s connect to the database and start enumerating other aspects of MariaDB.

#### Application/Service Enumeration

- First we need to connect to the database. 
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/1.png)
- Now that we are connected, we can look at what privileges we have as the wp user and get a better idea of how this MariaDB instance is configured.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/2.png)
- We don’t have "*" permissions, but SELECT, INSERT, UPDATE, and DELETE are a good starting point. Next, let’s take a look at some variables and see if we can find anything that stands out.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/3.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/4.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/5.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/6.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/7.png)
- From this one query we learned a few things. First, we found that the hostname is "kali". From this point on, we will refer to the MariaDB host as Zora. Next, we also learned that the tmp directory is in /tmp. We also confirm again that we are running MariaDB version 10.6.8 but we now also learn that the target architecture is x86_64. 
- The most interesting piece of information we can gather is that the plugin_dir is set to /usr/lib/mysql/plugin/. This directory is not 
standard for MariaDB. Let’s take note of that as it might become useful later on.
- Now that we have gathered some information, let’s see if we can find any exploits for our target MariaDB version.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/8.png)
- Unfortunately, none of these would work for our version of MariaDB. Let’s broaden the scope and see what we get for MySQL.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/9.png)
- When searching for MySQL vulnerabilities, we have to change our approach a bit. This time we are not looking for an exact version number that might be vulnerable to an exploit since MariaDB and MySQL use different version numbers. Instead, we are trying to see if we can identify a pattern in publicly disclosed exploits that may indicate a type of attack we could use.
- We notice that the words “UDF” and “User Defined” show up often. Let’s take a look at a more recent UDF exploit found in /usr/share/exploitdb/exploits/linux/local/46249.py.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/10.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/11.png)
- The exploit begins by referencing other research into UDF exploitation including a paper written on the subject.
- Reviewing this paper teaches us that a User Defined Function (UDF) is similar to a custom plugin for MySQL. It allows database administrators to create custom repeatable functions to accomplish specific objectives. Conveniently for us, UDFs are written in C or C++ and can run almost any code we want, including system commands.
- Researchers have discovered how to use standard MySQL (and MariaDB) functionality to create these plugins in ways that can be used to exploit systems. This specific exploit discusses using UDFs as ways to escalate privileges on a host. However, we should be able to use the same principle to get an initial shell. Some modifications will be required but before we start changing anything, let’s take a look at the code.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/12.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/13.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/14.png)
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/15.png)
- The first thing we notice is a shellcode variable defined on lines 40-45. The SQL query at line 71 obtains the plugin directory (remember this is the variable that we found was not standard on kali). Next, on line 92, the code dumps the shellcode binary content into a file within the plugin directory. Line 101 creates a function named sys_exec leveraging the uploaded binary file. Finally, 
the script checks if the function was successfully created on line 104 and if this is the case, the function is executed on line 113.
- Reading a bit more about the MySQL CREATE FUNCTION syntax suggests that the binary content of the shellcode variable is supposed to be a shared library that implements and exports the function(s) we want to create within the database. Essentially, this entire script is only running five commands. If we trim down the code to its essential MySQL commands, we obtain the following.
  ```bash
  select @@plugin_dir
  select binary 0xshellcode into dumpfile @@plugin_dir;
  create function sys_exec returns int soname udf_filename;
  select * from mysql.func where name='sys_exec' \G
  select sys_exec('cp /bin/sh /tmp/; chown root:root /tmp/sh; chmod +s /tmp/sh')
  ```
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/16.png)

### Attempting to Exploit the Database

- While the individual commands give us no reason for concern, we have no idea what the shellcode is doing. Instead, we will replace the shellcode with something that we are in control of. 
- The references in the exploit state that raptor_udf.c was used. A quick Google search reveals a relevant Exploit Database entry and a note at the bottom of the comments mentions a GitHub project that looks very promising.
- Let’s download the code, review it, and compile it.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/17.png)
- Opening up the lib_mysqludf_sys.c file shows us a fairly standard UDF library that allows for execution of system commands through the C/C++ system function.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/18.png)
- Now that we have reviewed the code, we will compile the shared library.Looking at the install.sh file, as a prerequisite for compilation we need to install libmysqlclient15-dev. In Kali Linux, this is the default-libmysqlclient-dev package, which can be installed with apt.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/19.png)

#### Why We Failed

- While the user does have permissions to run SELECT, INSERT, UPDATE, and DELETE, the wp user is missing the FILE permissions to be allowed to run dumpfile.
- To run dumpfile we need a user account with a higher level of permissions, such as the root user. Without this, we are stuck and 
cannot move forward with exploiting Zora using the current approach. The first logical option that comes to mind is to go back to Ajla and see if we can find root (or similar) MariaDB credentials.

## Targeting Poultry
### Poultry Enumeration

- We are assuming that Poultry is running Windows. We can become more confident by conducting some network enumeration with an Nmap scan. Should Nmap discover any applications, we can enumerate them as well.

#### Network Enumeration

- To run Nmap through ProxyChains, we will prepend the nmap command we want to run with proxychains. We will only scan the top 20 ports by using the –top-ports=20 flag and will conduct a connect scan with the -sT flag. SOCKS proxies require a TCP connection to be made 
and thus a half-open or SYN scan cannot be used with ProxyChains.
- Since SOCKS proxies require a TCP connection, ICMP cannot get through either and we must disable pinging with the -Pn flag. Finally, we will save the results to a file named poultry.nmap.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/20.png)
-  Nmap discovered ports 135, 139, 445, and 3389 to be open. However, port 53 is closed, which is commonly found open on domain controllers. This is most likely not the domain controller we are looking for, but the other ports still indicate that this is a Windows OS. The top 20 ports do not show any HTTP applications running, so let’s try to “exploit” this Windows machine by logging in via RDP with the credentials we discovered.

### Exploitation (Or Just Logging In)

- Now that we have a higher degree of confidence that Windows is running on this host and we found that RDP is open, we will use xfreerdp to connect to it.
- First, we must enable Remote Desktop in Win10.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/21.png)
- Now, we use Kali to connect to the Windows machine.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/22.png)

### Poultry Post-Exploitation Enumeration

- We will begin by gathering some basic information about the host such as the exact build of Windows, the hostname, local users, network information, and what services are running. We will start by running systeminfo.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/23.png)
- Since we were not able to do a full port scan, let’s find out what ports are open with the netstat command.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/24.png)
- Next, we can take a look at the services to see if anything interesting is running on this box. We can use the wmic command to list all the running services. We only want basic information for now like the name, displayname, pathname, and startmode.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/25.png)
- This is great information but there is way too much of it for us to review manually. We will narrow it down to services that are automatically started by piping the wmic command to findstr to look for the word “auto”. We also include the /i flag to make the search case insensitive.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/26.png)
- This output is better, but it’s not ideal. We can still take out services that are started from the c:\windows folder to get a list of non-standard services. This can be done by piping the command we have so far into findstr again and using the /v flag to ignore anything that contains the string “c:\windows”. We also use the /i flag again to make the search case insensitive.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/27.png)

### Unquoted Search Path Exploitation

- First, we will make a directory named poultry to work out of and copy a legitimate windows binary to it. The windows binary we will select is whoami.exe, which has a lower chance of being caught by AV considering that it is a well-known and legitimate utility.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/28.png)
- With the binary copied, we will generate a meterpreter payload to use with shellter. We will specify a Windows reverse TCP meterpreter payload to match our target operating system. Our Kali’s IPwill be specified in the LHOST option, and we will select port 80 with the LPORT option. Port 80 is selected in the hope of evading any potential outbound firewall restrictions. Next, we will encode the binary using the -e flag and specify an arbitrary number of encoding iterations with -i. Finally, we will output in raw format with the -f flag. The output of this command will be redirected to the met.bin file.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/29.png)

## Internal Network Enumeration

- To do so, we can write a quick one-liner to ping every possible host on the network using a for loop.
- To iterate through a command using a range of numbers, we can use the /L flag, which accepts a replaceable parameter (%i in our case) and the number to iterate through in the format of (start, step, end). Next, we will send a single ping for each host ( -n 1 ) and set a short timeout with the -w 200 flag. To obtain a tidy result, the output of the ping command will be redirected to the null interface ( via > nul ). Finally, if the ping command succeeded, we will echo the IP to indicate the host is up. 
- Please note however that this will only execute a ping sweep. That means that we cannot assume the results are complete as there may be live hosts that are configured to not respond to ICMP packets.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/30.png)
- Our sweep found five hosts, including the 192.168.50.10 gateway so we can ignore that for the time being. This leaves two more hosts of interest. We will conduct an Nmap scan for the top 1000 ports from Kali against the two hosts.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/31.png)

## Targeting the Jenkins Server
### Application Enumeration

- First, we can begin our enumeration by looking at the Document-Object Model (DOM) of the Jenkins login page. We will also look at the HTML source code later as it can be different than the DOM. To view the DOM, we right-click anywhere on the page and select Inspect Element.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/32.png)
- With the Firefox Web Developer Tools open, we right-click on the top HTML tag and select Expand All.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/33.png)
- A review of the DOM does not reveal any new information. We can see that the page is a basic HTML form.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/34.png)
- We will run a basic dirb scan to discover any potential hidden files. Jenkins will respond with a 403 for any file that we try to access when we are not logged in, so we will run our scan with the -w flag to continue scanning past the warning messages.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/35.png)
- Next, we login to Jenkins with the credentials we found earlier.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/36.png)

### Exploiting Jenkins

- Consulting the Jenkins documentation is enough to learn how to create a project that will allow us to execute system commands.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/37.png)
- When the new Item page opens, we will give the item a non-malicious sounding name like “Access”, select Freestyle project, and click OK.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/38.png)
- To have Jenkins execute a system command, we can use the Build configuration section.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/39.png)
- When the Command text box appears, we will enter in “whoami”. This will later change to other commands that we wish to execute. We will click Save when the command is entered in the textbox.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/40.png)
- Jenkins will then open the item’s main page. From here, we can select Build Now to run the command.
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/41.png)
- This will open up the “Console Output” page that displays errors and other information about the build. 
  ![Picture](../24.%20Assembling%20the%20Pieces%20Penetration%20Test%20Breakdown/Image/42.png)

