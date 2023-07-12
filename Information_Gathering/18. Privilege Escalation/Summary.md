# Content

- [Content](#content)
  - [Information Gathering](#information-gathering)
    - [Manual Enumeration](#manual-enumeration)
      - [Enumerating Users](#enumerating-users)
      - [Enumerating the Hostname](#enumerating-the-hostname)
      - [Enumerating the Operating System Version and Architecture](#enumerating-the-operating-system-version-and-architecture)
      - [Enumerating Running Processes and Services](#enumerating-running-processes-and-services)
      - [Enumerating Networking Information](#enumerating-networking-information)
      - [Enumerating Firewall Status and Rules](#enumerating-firewall-status-and-rules)
      - [Enumerating Scheduled Tasks](#enumerating-scheduled-tasks)
      - [Enumerating Installed Applications and Patch Levels](#enumerating-installed-applications-and-patch-levels)
      - [Enumerating Readable/Writable Files and Directories](#enumerating-readablewritable-files-and-directories)
      - [Enumerating Unmounted Disks](#enumerating-unmounted-disks)
      - [Enumerating Device Drivers and Kernel Modules](#enumerating-device-drivers-and-kernel-modules)
      - [Enumerating Binaries That AutoElevate](#enumerating-binaries-that-autoelevate)
    - [Automated Enumeration](#automated-enumeration)
  - [Windows Privilege Escalation Examples](#windows-privilege-escalation-examples)
    - [Understanding Windows Privileges and Integrity Levels](#understanding-windows-privileges-and-integrity-levels)
    - [Introduction to User Account Control (UAC)](#introduction-to-user-account-control-uac)
    - [User Account Control (UAC) Bypass: fodhelper.exe Case Study](#user-account-control-uac-bypass-fodhelperexe-case-study)
    - [Insecure File Permissions: Serviio Case Study.](#insecure-file-permissions-serviio-case-study)
    - [Leveraging Unquoted Service Paths](#leveraging-unquoted-service-paths)
    - [Windows Kernel Vulnerabilities: USBPcap Case Study](#windows-kernel-vulnerabilities-usbpcap-case-study)
  - [Linux Privilege Escalation Examples](#linux-privilege-escalation-examples)
    - [Understanding Linux Privileges](#understanding-linux-privileges)
    - [Insecure File Permissions: Cron Case Study](#insecure-file-permissions-cron-case-study)
    - [Kernel Vulnerabilities: CVE-2017-1000112 Case Study](#kernel-vulnerabilities-cve-2017-1000112-case-study)

  
## Information Gathering

- In these tests, the tester usually starts by gaining access to the system as a regular user or without special permissions. However, in order to realize the full effects of the attack, testers need to find ways to increase access to gain special permissions on the system.
- In this module, we assume that we already have unprivileged user access on a target running Windows and Linux operating systems, and will perform access enhancement techniques on these targets.
- Although each target can be considered unique due to differences in operating system versions, patch levels, and other factors, there are a number of general access enhancement methods. 
- These methods include looking for misconfigured services, insufficient file access restrictions on executables or services, direct vulnerabilities in the kernel, faulty software running with elevated permissions , sensitive information stored on local files, install scripts that may contain hard-coded credentials, and many other methods.

### Manual Enumeration
#### Enumerating Users

- When gaining initial access to a target, one of the first things we should identify is the user context. 
- The whoami command, available on both Windows and Linux platforms, is a good place to start.
- When run without parameters, whoami will display the username the shell is running as. - On Windows, we can pass the discovered username as an argument to the net user441 command to gather more information.
  ![Picture](../18.%20Privilege%20Escalation/Image/1.png)
- On Linux-based systems, we can use the id442 command to gather user context information.
  ![Picture](../18.%20Privilege%20Escalation/Image/2.png)
  - The output reveals the we are operating as the student user, which has a User Identifier (UID) and Group Identifier (GID) of 1000.
- To discover other user accounts on the system, we can use the net user command on 
Windows-based systems.
  ![Picture](../18.%20Privilege%20Escalation/Image/3.png)
- The output reveals other accounts, including the admin account.
- To enumerate users on a Linux-based system, we can simply read the contents of the 
/etc/passwd file.
  ![Picture](../18.%20Privilege%20Escalation/Image/4.png)
  - The passwd file lists several user accounts, including accounts used by various services on the 
target machine such as www-data, which indicates that a web server is likely installed.
- Enumerating all users on a target machine can help identify potential high-privilege user accounts 
we could target in an attempt to elevate our privileges.

#### Enumerating the Hostname

- A machine’s hostname can often provide clues about its functional roles. More often than not, the 
hostnames will include identifiable abbreviations such as web for a web server, db for a database 
server, dc for a domain controller, etc.
- We can discover the hostname with the aptly-named hostname command, which is installed 
on both Windows and Linux.
- Let's run it on Windows first.
  ![Picture](../18.%20Privilege%20Escalation/Image/5.png)
- Then on Linux.
  ![Picture](../18.%20Privilege%20Escalation/Image/6.png)

#### Enumerating the Operating System Version and Architecture

- At some point during the privilege escalation process, we may need to rely on kernel exploits that specifically exploit vulnerabilities in the core of a target’s operating system. 
- These types of exploits are built for a very specific type of target, specified by a particular operating system and version combination. 
- On the Windows operating system, we can gather specific operating system and architecture information with the systeminfo utility.
- We can also use findstr along with a few useful flags to filter the output. Specifically, we can match patterns at the beginning of a line with /B and specify a particular search string with /C:.
  ```bash
  systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/7.png)
- On Linux, the /etc/issue and /etc/*-release files contain similar information. We can also issue the 
uname -a command.
  ```bash
  cat /etc/issue
  cat /etc/issue
  uname -a
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/8.png)

#### Enumerating Running Processes and Services 

- Next, let’s take a look at running processes and services that may allow us to elevate our privileges. 
- For this to occur, the process must run in the context of a privileged account and must either have insecure permissions or allow us to interact with it in unintended ways.
- We can list the running processes on Windows with the tasklist command. The /SVC flag will return processes that are mapped to a specific Windows service.
  ```bash
  tasklist /SVC
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/9.png)
- On Linux, we can list system processes (including those run by privileged users) with the ps command. We’ll use the a and x flags to list all processes with or without a tty452 and the u flag to list the processes in a user-readable format.
  ```bash
  ps axu
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/10.png)

#### Enumerating Networking Information

- The next step in our analysis of the target host is to review available network interfaces, routes, 
and open ports.
- This information can help us determine if the compromised target is connected to multiple networks and therefore could be used as a pivot. In addition, the presence of specific virtual interfaces may indicate the existence of virtualization or antivirus software.
- We can begin our information gathering on the Windows operating system with ipconfig, using the /all flag to display the full TCP/IP configuration of all adapters.
  ![Picture](../18.%20Privilege%20Escalation/Image/11.png)
- To display the networking routing tables, we will use the route command followed by the print argument.
  ```bash
  route print
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/12.png)
- Finally, we can use netstat to view the active network connections. Specifying the a flag will display all active TCP connections, the n flag allows us to display the address and port number in a numerical form, and the o flag will display the owner PID of each connection.
  ```bash
  netstat -ano
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/13.png)
- Similar commands are available on a Linux-based host. Depending on the version of Linux, we can list the TCP/IP configuration of every network adapter with either ifconfig or ip.
- Both commands accept the a flag to display all information available.
  ![Picture](../18.%20Privilege%20Escalation/Image/14.png)
- We can display network routing tables with either route458 or routel, depending on the Linux flavor and version.
  ![Picture](../18.%20Privilege%20Escalation/Image/15.png)
- Finally, we can display active network connections and listening ports with either netstat or 
ss, both of which accept the same arguments.
- For example, we can list all connections with -a, avoid hostname resolution (which may stall the command execution) with -n, and list the process name the connection belongs to with -p. We can combine the arguments and simply run ss -anp.
  ```bash
  ss -anp 
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/16.png)

#### Enumerating Firewall Status and Rules

- Generally speaking, a firewall’s state, profile, and rules are only of interest during the remote exploitation phase of an assessment. However, this information can be useful during privilege escalation. 
- In addition, we can gather information about inbound and outbound port filtering during this phase to facilitate port forwarding and tunneling when it’s time to pivot to an internal network.
- On Windows, we can inspect the current firewall profile using the netsh command.
  ```bash
  netsh advfirewall show currentprofile
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/17.png)
- We can list firewall rules with the netsh command using the following syntax.
  ```bash
  netsh advfirewall firewall show rule name=all
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/18.png)

#### Enumerating Scheduled Tasks

- Attackers commonly leverage scheduled tasks in privilege escalation attacks.
- We can create and view scheduled tasks on Windows with the schtasks466 command. The /query argument displays tasks and /FO LIST sets the output format to a simple list. We can also use /V to request verbose output.
  ```bash
  schtasks /query /fo LIST /v
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/19.png)
- The Linux-based job scheduler is known as Cron. 
- Scheduled tasks are listed under the /etc/cron.* directories, where * represents the frequency the task will run on. For example, tasks that will be run daily can be found under /etc/cron.daily. Each script is listed in its own subdirectory.
  ![Picture](../18.%20Privilege%20Escalation/Image/20.png)
- It is worth noting that system administrators often add their own scheduled tasks in the /etc/crontab file.
- These tasks should be inspected carefully for insecure file permissions as most jobs in this particular file will run as root.
  ![Picture](../18.%20Privilege%20Escalation/Image/21.png)

#### Enumerating Installed Applications and Patch Levels

- At some point, we may need to leverage an exploit to escalate our local privileges. If so, our search for a working exploit begins with the enumeration of all installed applications, noting the version of each (as well as the OS patch level on Windows-based systems). We can use this 
information to search for a matching exploit.
- Manually searching for this information could be very time consuming and ineffective. However, we can leverage the very powerful Windows-based utility, wmic to automate this process on Windows systems.
- We can use wmic with the product WMI class argument followed by get, which, as the name states, is used to retrieve specific property values. We can then choose the properties we are interested in, such as name, version, and vendor.
  ```bash
  wmic product get name, version, vendor
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/22.png)
- Similarly, and more importantly, wmic can also be used to list system-wide updates by querying the Win32_QuickFixEngineering (qfe) WMI class.
  ```bash
  wmic qfe get Caption, Description, HotFixID, InstalledOn
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/23.png)
- Linux-based systems use a variety of package managers. For example, Debian-based Linux distributions use dpkg while Red Hat based systems use rpm.
- To list applications installed (by dpkg) on our Debian system, we can use dpkg -l.
  ![Picture](../18.%20Privilege%20Escalation/Image/24.png)

#### Enumerating Readable/Writable Files and Directories

- As we previously mentioned, files with insufficient access restrictions can create a vulnerability that can grant an attacker elevated privileges. This most often happens when an attacker can modify scripts or binary files that are executed under the context of a privileged account.
- In the following example, we will demonstrate how to use AccessChk to find a file with insecure file permissions in the Program Files directory. Please note that the target binary file was simply created for the purposes of this exercise. 
- Specifically, we will enumerate the Program Files directory in search of any file or directory that allows the Everyone476 group write permissions.
- We will use -u to suppress errors, -w to search for write access permissions, and -s to perform a recursive search. The additional options are also worth exploring as this tool is quite useful.
  ```bash
  accesschk.exe -uws "Everyone" "C:\Program Files"
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/25.png)
- On Linux operating systems, we can use find477 to identify files with insecure permissions.
- In the example below, we are searching for every directory writable by the current user on the target system. We search the whole root directory (/) and use the -writable argument to specify the attribute we are interested in. We also use -type d to locate directories, and we filter errors with 2>/dev/null.
  ```bash
  find / -writable -type d 2>/dev/null
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/26.png)

#### Enumerating Unmounted Disks 

- On most systems, drives are automatically mounted at boot time. Because of this, it’s easy to forget about unmounted drives that could contain valuable information. We should always look for unmounted drives, and if they exist, check the mount permissions.
- On Windows-based systems, we can use mountvol to list all drives that are currently mounted as well as those that are physically connected but unmounted.
  ![Picture](../18.%20Privilege%20Escalation/Image/27.png)
- On Linux-based systems, we can use the mount command to list all mounted filesystems. In addition, the /etc/fstab480 file lists all drives that will be mounted at boot time.
  ![Picture](../18.%20Privilege%20Escalation/Image/28.png)
- The output reveals a swap partition and the primary ext4 disk of this Linux system. Furthermore, we can use lsblk to view all available disks.
  ![Picture](../18.%20Privilege%20Escalation/Image/29.png)

#### Enumerating Device Drivers and Kernel Modules

- On Windows, we can begin our search with the driverquery482 command. We’ll supply the /v argument for verbose output as well as /fo csv to request the output in CSV format.
- To filter the output, we will run this command inside a powershell session. Within PowerShell, we will pipe the output to the ConvertFrom-Csv cmdlet as well as Select-Object, which will allow us to select specific object properties or sets of objects including Display Name, Start Mode, and Path.
  ```bash
  driverquery.exe /v /fo csv | ConvertFrom-CSV | Select-Object ‘Display Name’, ‘Start Mode’, Path
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/30.png)
- On Linux, we can enumerate the loaded kernel modules using lsmod without any additional arguments.
  ![Picture](../18.%20Privilege%20Escalation/Image/31.png)
- Once we have the list of loaded modules and identify those we want more information about, like libata in the above example, we can use modinfo to find out more about the specific module. 
  ![Picture](../18.%20Privilege%20Escalation/Image/32.png)

#### Enumerating Binaries That AutoElevate

- Later in this module, we will explore various methods of privilege escalation. However, there are a few specific enumerations we should cover in this section that could reveal interesting OS-specific “shortcuts” to privilege escalation.
- Normally, when running an executable, it inherits the permissions of the user that runs it. However, if the SUID permissions are set, the binary will run with the permissions of the file owner. This means that if a binary has the SUID bit set and the file is owned by root, any local user will be able to execute that binary with elevated privileges.
- We can use the find command to search for SUID-marked binaries. In this case, we are starting our search at the root directory (/), looking for files (-type f) with the SUID bit set, (-perm -u=s) and discarding all error messages (2>/dev/null).
  ```bash
  find / -perm -u=s -type f 2>/dev/null
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/33.png)

### Automated Enumeration

- Obviously, each operating system contains a wealth of information that can be used for further attacks. Regardless of the target operating system, collecting this detailed information manually can be rather time-consuming. Fortunately, we can use various scripts to automate this process.
- On Windows, one such script is windows-privesc-check, which can be found in the windows-privesc-check Github repository.
- The repository already includes a Windows executable generated by PyInstaller, but it can also be rebuilt as needed.
- Running the executable with the -h flag presents us with the following help menu.
  ```bash
  windows-privesc-check2.exe -h
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/34.png)
- This tool accepts many options, but we will walk through some quick examples. First, we will list information about the user groups on the system. We’ll specify the self-explanatory --dump to view output, and -G to list groups.
  ```bash
  windows-privesc-check2.exe --dump -G
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/35.png)
- Similar to windows-privesc-check on Windows targets, we can also use unix_privesc_check on UNIX derivatives such as Linux. We can view the tool help by running the script without any arguments.
  ![Picture](../18.%20Privilege%20Escalation/Image/36.png)
- As shown in the listing above, the script supports “standard” and “detailed” mode. Based on the provided information, the standard mode appears to perform a speed-optimized process and should provide a reduced number of false positives. Therefore, in the following example we will use the standard mode and redirect the entire output to a file called output.txt.
  ```bash
  unix-privesc-check standard > output.txt
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/37.png)
  ![Picture](../18.%20Privilege%20Escalation/Image/38.png)

## Windows Privilege Escalation Examples
### Understanding Windows Privileges and Integrity Levels

- Privileges on Windows operating systems refer to the permissions granted to a specific account for performing system-related local operations. These privileges allow actions such as modifying the file system, adding users, shutting down the system, and more.
- To enforce these privileges, Windows uses access tokens. When a user is authenticated, Windows generates an access token that is assigned to that user. The access token contains information about the user's security context, including their privileges.
- To uniquely identify these tokens, Windows assigns them a security identifier (SID), which is a unique value given to each object, including tokens, user accounts, and groups. The Windows Local Security Authority is responsible for generating and maintaining these SIDs.
- In addition to privileges, Windows implements an integrity mechanism, which is a crucial component of its security architecture. This mechanism assigns integrity levels to application processes and securable objects. Integrity levels determine the level of trust the operating system has in running applications or objects. For example, the integrity level dictates the actions an application can perform, such as reading from or writing to the file system. Certain APIs may also be blocked based on specific integrity levels.
- Starting from Windows Vista, processes can run on four integrity levels.
  - System integrity process: Has SYSTEM rights.
  - High integrity process: Has administrative rights.
  - Medium integrity process: Has standard user rights.
  - Low integrity process: Has very restricted rights and is often used for sandboxed processes.

### Introduction to User Account Control (UAC)

- User Account Control (UAC) is an access control system introduced by Microsoft with Windows Vista and Windows Server 2008. While UAC has been discussed and investigated for quite a long time now, it is important to stress that Microsoft does not consider it to be a security boundary. 
- Rather, UAC forces applications and tasks to run in the context of a non-administrative account until an administrator authorizes elevated access.
- Even while logged in as an administrative user, the account will have two security tokens, one running at a medium integrity level and the other at high integrity level. UAC acts as the separation mechanism between those two integrity levels.
- To see integrity levels in action, let’s first login as the admin user, open a command prompt, and run the whoami /groups command.
  ![Picture](../18.%20Privilege%20Escalation/Image/39.png)
- Let’s attempt to change the password for the admin user from this command prompt.
  ```bash
  net user Thai_SE161457_Win10 hello
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/40.png)
- In order to change the admin user’s password, we must switch to a high integrity level even if we are logged in with an administrative user. In our example, one way to do this is through powershell.exe with the Start-Process cmdlet specifying the “Run as administrator” option.
  ```bash
  powershell.exe Start-Process cmd.exe -Verb runAs
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/41.png)
- After submitting this command and accepting the UAC prompt, we are presented with a new high integrity cmd.exe process.
- Let’s check our integrity level using the whoami utility using the /groups argument and attempt to change the password again.
  ! [Picture](../18.%20Privilege%20Escalation/Image/42.png)

### User Account Control (UAC) Bypass: fodhelper.exe Case Study

- UAC can be bypassed in various ways. In this first example, we will demonstrate a technique that allows an administrator user to bypass UAC by silently elevating our integrity level from medium to high.
- Most of the publicly known UAC bypass techniques target a specific operating system version. 
- In this case, the target is our lab client running Windows 10 build 1709. We will leverage an interesting UAC bypass based on fodhelper.exe, a Microsoft support application responsible for managing language changes in the operating system. Specifically, this application is launched whenever a local user selects the “Manage optional features” option in the “Apps & features” Windows Settings screen.
  ![Picture](../18.%20Privilege%20Escalation/Image/43.png)
- We’ll begin our analysis by running the C:\Windows\System32\fodhelper.exe binary, which presents the Manage Optional Features settings pane.
  ![Picture](../18.%20Privilege%20Escalation/Image/44.png)
- In order to gather detailed information regarding the fodhelper integrity level and the permissions required to run this process, we will inspect its application manifest.
- The application manifest is an XML file containing information that lets the operating system know how to handle the program when it is started. We’ll inspect the manifest with the sigcheck utility from Sysinternals,513 passing the -a argument to obtain extended information and -m to dump the manifest.
  ```bash
  sigcheck.exe -a -m C:\Windows\System32\fodhelper.exe
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/45.png)
- After starting procmon.exe, we’ll run fodhelper.exe again and set filters to specifically focus on the activities performed by our target process.
  ![Picture](../18.%20Privilege%20Escalation/Image/46.png)

### Insecure File Permissions: Serviio Case Study.

- As previously mentioned, a common way to elevate privileges on a Windows system is to exploit insecure file permissions on services that run as nt authority\system.
- This type of vulnerability exists on our Windows client. Let’s validate the vulnerability and exploit it.
- In one of the previous sections, we showed how to list running services with tasklist. Alternatively, we could use the PowerShell Get-WmiObject cmdlet with the win32_service WMI class. In this example, we will pipe the output to Select-Object to display the fields we are interested in and use Where-Object to display running services ({$_.State -like ‘Running’}).
  ```bash
  Get-WmiObject win32_service | Select-Object Name, State, PathName | Where-Object {$_.State -like 'Running'}
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/47.png)

### Leveraging Unquoted Service Paths

- Another interesting attack vector that can lead to privilege escalation on Windows operating systems revolves around unquoted service paths.
- We can use this attack when we have write permissions to a service’s main directory and subdirectories but cannot replace files within them. 
- As we have seen in the previous section, each Windows service maps to an executable file that will be run when the service is started. Most of the time, services that accompany third party software are stored under the C:\Program Files directory, which contains a space character in its name. This can potentially be turned into an opportunity for a privilege escalation attack.
- When using file or directory paths that contain spaces, the developers should always ensure that they are enclosed by quotation marks. This ensures that they are explicitly declared. However, when that is not the case and a path name is unquoted, it is open to interpretation. Specifically, in the case of executable paths, anything that comes after each whitespace character will be treated 
as a potential argument or option for the executable.
- For example, we could name our executable Program.exe and place it in C:\, or name it My.exe and place it in C:\Program Files. However, this would require some unlikely write permissions since standard users do not have write access to these directories by default.
- It is more likely that the software’s main directory (C:\Program Files\My Program in our example) or subdirectory (C:\Program Files\My Program\My service) is misconfigured, allowing us to plant a malicious My.exe binary.
- Although this vulnerability requires a specific combination of requirements, it is easily exploitable and a privilege escalation attack vector worth considering.

### Windows Kernel Vulnerabilities: USBPcap Case Study

- When attempting to exploit system-level software (such as drivers or the kernel itself), we must pay careful attention to several factors including the target’s operating system, version, and architecture. Failure to accurately identify these factors can trigger a Blue Screen of Death while running the exploit. This can adversely affect the client’s production system and deny us access to a potentially valuable target.
- Considering the level of care we must take, in the following example we will first determine the version and architecture of the target operating system.
  ```bash
  systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/48.png)
- The output of the command reveals that our target is running Windows 10 Pro an x86 processor.
- At this point, we could attempt to locate a native kernel vulnerability for Windows 10 Pro x86 and use it to elevate our privileges. However, third-party driver exploits are more common. As such, we should always attempt to investigate this attack surface first before resorting to more difficultattacks.
- To do this, we’ll first enumerate the drivers that are installed on the system.
  ```bash
  driverquery /v 
  ```
  ![Picture](../18.%20Privilege%20Escalation/Image/49.png)
  ![Picture](../18.%20Privilege%20Escalation/Image/50.png)

## Linux Privilege Escalation Examples
### Understanding Linux Privileges

- Before discussing privilege escalation techniques, let’s take a moment to briefly discuss Linux privileges, access controls, and users.
- One of the defining features of Linux and other UNIX derivatives is that most resources, including files, directories, devices, and even network communications are represented in the filesystem.
- Put colloquially, “everything is a file”. Every file (and by extension every element of a Linux system) abides by user and group permissions542 based on three primary abilities: read, write, and execute.

### Insecure File Permissions: Cron Case Study

- Unless a centralized credential system such as Active Directory or LDAP is used, Linux passwords are generally stored in /etc/shadow, which is not readable by normal users. Historically however, password hashes, along with other account information, were stored in the world-readable file /etc/passwd. 
- For backwards compatibility, if a password hash is present in the second column of a /etc/passwd user record, it is considered valid for authentication and it takes precedence over the respective entry in /etc/shadow if available. This means that if we can write into the /etc/passwd file, we can effectively set an arbitrary password for any account.
- Let’s demonstrate this. In a previous section we showed that our Kali client may be vulnerable to privilege escalation due to the fact that the /etc/passwd permissions were not set correctly. In order to escalate our privileges, we are going to add another superuser (root2) and the corresponding password hash to the /etc/passwd file. We will first generate the password hash with the help of openssl and the passwd argument. By default, if no other option is specified, openssl will generate a hash using the crypt algorithm,546 which is a supported hashing mechanism for Linux authentication. Once we have the generated hash, we will add a line to /etc/passwd using the appropriate format.
  ![Picture](../18.%20Privilege%20Escalation/Image/51.png)
- The “root2” user and the password hash in our /etc/passwd record were followed by the user id (UID) zero and the group id (GID) zero. These zero values specify that the account we created is a superuser account on Linux. 
- Finally, in order to verify that our modifications were valid, we used the su command to switch our standard user to the newly created root2 account and issued the id command to show that we indeed had root privileges.

### Kernel Vulnerabilities: CVE-2017-1000112 Case Study

- Kernel exploits are an excellent way to escalate privileges, but success may depend on matching not only the target’s kernel version but also the operating system flavor, including Debian, Redhat, Gentoo, etc.
- Similar to our Windows examples, this section of the module will not be reproducible on your dedicated client, but you will be able to use this technique on various hosts inside the lab environment.
- To demonstrate this attack vector, we will first gather information about our target by inspecting the /etc/issue file. As discussed earlier in the module, this is a system text file that contains a message or system identification to be printed before the login prompt on Linux machines.
  ![Picture](../18.%20Privilege%20Escalation/Image/52.png)
- Next, we will inspect the kernel version and system architecture using standard system commands.
  ![Picture](../18.%20Privilege%20Escalation/Image/53.png)
- Armed with this information, we can use searchsploit on our local Kali system to find kernel exploits matching the target version.
  ![Picture](../18.%20Privilege%20Escalation/Image/54.png)