# Content

- [Content](#content)
  - [Wordlists](#wordlists)
    - [Standard Wordlists](#standard-wordlists)
      - [Tool cewl](#tool-cewl)
        - [The way to work](#the-way-to-work)
        - [Demo](#demo)
      - [Tool John the Ripper](#tool-john-the-ripper)
        - [The way to work](#the-way-to-work-1)
        - [Demo](#demo-1)
  - [Brute Force Wordlists](#brute-force-wordlists)
    - [Tool Crunch](#tool-crunch)
      - [The way to work](#the-way-to-work-2)
      - [Demo](#demo-2)
  - [Common Network Service Attack Methods](#common-network-service-attack-methods)
    - [HTTP htaccess Attack with Medusa](#http-htaccess-attack-with-medusa)
      - [The way to work](#the-way-to-work-3)
      - [Demo](#demo-3)
    - [Remote Desktop Protocol Attack with Crowbar](#remote-desktop-protocol-attack-with-crowbar)
      - [The way to work](#the-way-to-work-4)
      - [Demo](#demo-4)
    - [SSH Attack with THC-Hydra](#ssh-attack-with-thc-hydra)
      - [The way to work](#the-way-to-work-5)
      - [Demo](#demo-5)
  - [Leveraging Password Hashes](#leveraging-password-hashes)
    - [Retrieving Password Hashes](#retrieving-password-hashes)
      - [Tool hashid](#tool-hashid)
        - [The way to work](#the-way-to-work-6)
        - [Demo](#demo-6)
      - [Tool mimikatz](#tool-mimikatz)
        - [The way to work](#the-way-to-work-7)
        - [Demo](#demo-7)
    - [Passing the Hash in Windows](#passing-the-hash-in-windows)
      - [Technique Pass the Hash](#technique-pass-the-hash)
    - [Password Cracking](#password-cracking)

  
## Wordlists

- Wordlists, also called dictionary files, are simple text files that contain words for use as input to programs designed to check passwords. When considering a dictionary attack, accuracy is often more important than scope, which means it's more important to generate a list of related password words than to generate a huge and common word list. As a result, many word lists are based on a common theme, such as popular cultural references, specific industries, or geographies, and are fenced to contain common passwords.
- Kali Linux includes some of these dictionary files in the /usr/share/wordlists/ directory and many more are stored online. When conducting a password attack, it can be tempting to just use these pre-built lists. However, we can be a lot more efficient in our approach if we take the time to carefully build our custom lists. In this section, we'll look at tools and methods for creating effective word lists.
  ![Picture](../19.%20Password%20Attacks/Image/1.png)

### Standard Wordlists

- We can increase the effectiveness of our wordlists by adding words and phrases specific to our target organization. 
- For example, one can consider the company MegaCorp One, a company active in the field of nanotechnology. The company's website, www.megacorpone.com, lists the products it sells, including the Nanobot. In a hypothetical evaluation, we identified the low-level password as Nanobot93. Assuming that this might be a common password pattern for this company, we want to create a custom wordlist to identify other passwords with a similar pattern, possibly using other product names.
- We will use a tool like cewl.

#### Tool cewl

##### The way to work

- The cewl tool (also known as Custom Wordlist Generator) is a tool used to create custom word lists. It is commonly used in penetration testing and dictionary attacks.
- Cewl will scan through a provided web page and search for words and phrases based on the formats, parameters and options entered. It can collect words according to certain rules, such as appearing at least a few times, or only from specific links on a web page.

##### Demo

- We will find words with a minimum of six characters (-m 6), and writes (-w) the wordlist to a custom file (megacorp-cewl.txt) from the MegaCorp One website (www.megacorpone.com).
  ```bash
  cewl www.megacorpone.com -m 6 -w megacorp-cewl.txt
  ```
  ![Picture](../19.%20Password%20Attacks/Image/2.png)
- Found several product names, including Nanobot, and suggested that other product names could be used as passwords. 
- However, these words alone would be very weak passwords and do not meet the usual rules for setting up passwords. 
- These rules often require the use of ```bash both upper and lower case letters, the use of numbers, and possibly the use of special characters```. Based on the found password (Nanobot93), it can be inferred that the requirement to set up a password for megacorpone is to use at least two numbers in the password and may require (although very rarely) the use of a password at the end of the password.
- So we need to create a custom wordlist that includes the words we found, but also includes the words we found with two numbers added to the end of the word.
- Once we know the low level password is "Nanobot93", using the "cewl" tool to find words that appear at least 6 characters has another purpose.
- In the quoted example, after running the command "cewl www.megacorpone.com -m 6 -w megacorp-cewl.txt", the "cewl" tool is used to collect words with at least 6 characters from the page website of MegaCorp One (www.megacorpone.com). This helps us to identify words through scanning and analyzing web page content.
- When we collect words from this website, we are not only looking for words like ```bash Nanobot```, but we also collect other words like ```bash Nanotechnology```, ```bash Nanomite```, ```bash Nanoprobe```, ```bash Nanoprocessors```, ```bash NanoTimes``` and many other products related to the company MegaCorp One.
- Depend on the password we know: ```bash Nanobot93 ``` we will add two number after each password in file megacorp-cewl.txt.
- We will use tool like John the Ripper to create a custom wordlist.

#### Tool John the Ripper

##### The way to work

- Users of John the Ripper can gather information by extracting a password file from a system or database. This information typically contains user accounts and encrypted passwords.
- After gathering information, users can create a list of dictionaries using predefined rules. These rules can be regular string transformations applied to the original dictionary to create variations.

##### Demo

- We will add the rule which append the two-digit sequence of numbers from (double) zero to ninety-nine after each word in our wordlist.
  ![Picture](../19.%20Password%20Attacks/Image/3.png)
- Now that the rule has been added to the configuration file. We will add the rule to the wordlist and create a new dictionary.
  ```bash
  john --wordlist=megacorp-cewl.txt --rules --stdout > mutated.txt
  grep Nanobot mutated.txt
  ```
  - "john": This is the main command to launch John the Ripper
  - "--wordlist=megacorp-cewl.txt": This parameter defines the root dictionary used as "megacorp-cewl.txt". 
  - "--rules": This parameter tells John the Ripper to apply transformation rules to the list of dictionaries. 
  - "--stdout": This parameter allows John the Ripper to output to standard output (stdout) instead of writing to a file.
  - "> mutated.txt": The ">" sign is used to redirect output from stdout to a new file named "mutated.txt". 
  ![Picture](../19.%20Password%20Attacks/Image/4.png)
- The resulting file contains over 46000 password entries due to the multiple mutations performed on the passwords. 
- One of the passwords is “Nanobot93”, which matches the password we discovered earlier in our hypothetical assessment. 
- Given the assumptions about the MegaCorp One password policy, this wordlist could produce results in a dictionary attack.

## Brute Force Wordlists

- The difference between a dictionary attack and a brute force attack on passwords.
  - Dictionary attack is the process of trying all the words in a dictionary to find the right password. It is based on the assumption that the user uses a password that is common or already appears in the dictionary. This means that if the password is not in the dictionary, the dictionary attack will fail.
  - The brute force attack computes and checks every possible combination of characters to form a password until it finds the right one. This method guarantees results, but is very time consuming. The brute force attack time depends on the length and complexity of the password as well as the computing power of the testing system.
- For example, consider a scenario that reveals a very specific password enforcement policy.
  ```bash
  cat dumped.pass.txt
  ```
  ![Picture](../19.%20Password%20Attacks/Image/5.png)
- Looking at the passwords, we notice the following pattern in the password structure.
  ![Picture](../19.%20Password%20Attacks/Image/6.png)
- We have the format of the password, which is a combination of two words, each word is capitalized, and the two words are separated by a number. So we will use tool like Crunch to create a custom wordlist.

### Tool Crunch

#### The way to work

- Crunch is used to generate words or strings of characters that can be used to create password lists or word lists. Crunch allows you to define rules and patterns to create different representations of words or strings of characters.

#### Demo

- We use Crunch to create a wordlist.
  ```bash
  crunch 8 8 -t ,@@^^%%%
  ```
  - The minimum and maximum length of the password to be eight characters (8 8) 
  - Described the password structure in the form "-t ,@@^^%%%". 
    - "," for uppercase letters.
    - "@" for lowercase letters.
    - "^" for characters special self.
    - "%" for numbers.
  ![Picture](../19.%20Password%20Attacks/Image/7.png)

## Common Network Service Attack Methods

- Now that we understand how to create effective wordlists for various situations, we can discuss how they can be used for password attacks against common network services.

### HTTP htaccess Attack with Medusa

#### The way to work

- Tool Medusa is a password attack tool used to try accounts and passwords in system authentication. Medusa's mechanism of action focuses on performing a brute-force attack by repeatedly sending authentication requests with different accounts and passwords for the purpose of checking if the information is correct. which authentication is appropriate.
- Medusa works using a list of possible accounts and passwords, selected from data sources provided by the user or automatically generated from predefined rules. Then, Medusa sends authentication requests to the target IP address via protocol like HTTP, FTP, Telnet, SSH and many more.
- When Medusa receives a response from the target server, it analyzes the response to determine if the credentials are correct. If it is determined that a correct account and password has been found, Medusa will notify the user again of the finding of a valid account/password pair.

#### Demo

- First, we will set up our target. We will start apache service in Kali Linux.
  ```bash
  service apache2 start
  ```
  ![Picture](../19.%20Password%20Attacks/Image/8.png)
- Our wordlist of choice for this example will be 
/usr/share/wordlists/rockyou.txt.gz, which we must first decompress with gunzip.
  ```bash
  sudo gunzip /usr/share/wordlists/rockyou.txt.gz
  ```
- Next, we will launch medusa and initiate the attack against the htaccess-protected URL (-m DIR:/root) on our target host with -h 192.168.50,163. We will attack the admin user (-u root) with passwords from our rockyou wordlist file (-P /usr/share/wordlists/rockyou.txt) and will, of course, use an HTTP authentication scheme (-M).
  ```bash
  medusa -h 192.168.50.163 -u root -P /usr/share/wordlists/rockyou.txt -M http -m DIR:/root
  ```
  ![Picture](../19.%20Password%20Attacks/Image/9.png)

### Remote Desktop Protocol Attack with Crowbar

#### The way to work

- Crowbar is a password cracking tool used to attack the system with the aim of breaking encrypted passwords. Crowbar's mechanism of action is usually done by trying each value in a list of possible passwords for a particular account, until the correct password is found.
- Crowbar often uses brute-force techniques to try all possible password possibilities. It will continuously try different strings of characters, from regular dictionaries to random characters, until it finds a password that matches the requested login information.
- Theoretically the mechanism of crowbar and medusa is the same

#### Demo

- In windows machine, we open rdp service.
  ![Picture](../19.%20Password%20Attacks/Image/10.png)
- In kali machine, we create two file: user.txt and pass.txt
  ![Picture](../19.%20Password%20Attacks/Image/11.png)
- To invoke crowbar, we will specify the protocol (-b), the target server (-s), a username (-u), a wordlist (-C), and the number of threads (-n).
  ```bash
  crowbar -b rdp -s 192.168.50.10/32 -U user.txt -C pass.txt -n 1
  ```
  - -b rdp: Specify the target protocol for the attack as RDP.
  - -s 192.168.50.10/32: The IP address of the target RDP server.
  - -U user.txt: Path to the file user.txt containing a list of usernames (usernames) to try.
  - -C pass.txt: Path to the file pass.txt containing the list of passwords (passwords) to try.
  - -n 1: Specifies the maximum number of parallel connections allowed.
  ![Picture](../19.%20Password%20Attacks/Image/12.png)

### SSH Attack with THC-Hydra

#### The way to work

- THC-Hydra is a powerful and popular password hacking tool. It is used to perform password brute force attacks on protocols such as SSH, FTP, Telnet, HTTP and many others. This tool allows you to try a series of different passwords from a list or dictionary to guess the correct password and break into the system.
- The mechanism of action of THC-Hydra is based on the principle of password exhaustion. It will try each password in the provided list or dictionary and send connection requests to the target server. When credentials are sent (e.g. username and password), the tool checks to see if the credentials are correct. This process repeats until a correct password is found or the list is exhausted.

#### Demo

- In kali machine, i will open service ssh.
  ```bash
  sudo systemctl start ssh.service
  ```
  ![Picture](../19.%20Password%20Attacks/Image/13.png)
- We will attack our Kali VM. We will use the SSH protocol on our local machine ssh://192.168.50.156, focus on the kali user (-l kali), and again use the rockyou wordlist (-P).
  ```bash
  hydra -l kali -P /usr/share/wordlists/rockyou.txt ssh://192.168.50.156
  ```
  - -l kali: This is the -l option to specify the kali username or username.
  - -P /usr/share/wordlists/rockyou.txt: The -P option is used to specify the path to the password dictionary list (rockyou.txt) used during the attack.
  - ssh://192.168.50.156: This is the target endpoint of the SSH attack, with an IP address of 192.168.50.156 (localhost).
  ![Picture](../19.%20Password%20Attacks/Image/14.png)

## Leveraging Password Hashes
### Retrieving Password Hashes

- Systems often store passwords as hashes to improve security. Instead of storing passwords as plain text, modern authentication mechanisms often store them as hashes for added security. This applies to operating systems, network hardware, and many other systems.
- When authentication takes place, the user-provided password is hashed and compared with the previously stored hash value. However, determining a particular hash without further information about the program or mechanism that generates it can be very difficult, sometimes even impossible. The Openwall website can help determine the origin of different password hashes.
- When trying to determine the type of password hash, there are three important properties of the hash to consider. It is the length of the hash, the character set used in the hash, and the special characters used in the hash.
- A useful tool that can assist with hash type identification is hashid.

#### Tool hashid

##### The way to work

- HashID is a tool used to identify the type of hash algorithm used in a hash string of unknown origin. It can recognize popular hash algorithms like MD5, SHA-1, SHA-256 and many others.
- HashID's mechanism of action is based on comparing the hash value with the known constants of each algorithm. When you give it a hash string, HashID checks that string against a list of hash patterns typical of each algorithm. If a match is found, it determines the corresponding hash algorithm.

##### Demo

- To use it, we simply run the tool and paste in the hash we wish to identify.
  ```basg
  hashid c43ee559d69bc7f691fe2fbfe8a5ef0a
  hashid '$6$l5bL6XIASslBwwUD$bCxeTlbhTH76wE.bI66aMYSeDXKQ8s7JNFwa1s1KkTand6ZsqQKAF3G0tHD9bd59e5NAz/s7DQcAojRTWNpZX0'
  ```
  ![Picture](../19.%20Password%20Attacks/Image/15.png)
- Next, let’s retrieve and analyze a few hashes on our Kali Linux system. Many Linux systems have the user password hashes stored in the /etc/shadow file, which requires root permissions to read.
  ```bash
  sudo grep root /etc/shadow
  ```
  ![Picture](../19.%20Password%20Attacks/Image/16.png)
- When storing passwords, instead of just computing the hash from the original password, the system generates a random salt value and combines it with the password. The password hash calculation will use both the password and the salt value to generate the final stored password hash.
- The use of salt increases the randomness of the password value prior to hash calculation, greatly reducing the hash's viability in the precomputed table. This makes it more difficult to attack by hash lookup.
- LSASS is a service in the Windows operating system whose main task is to authenticate users by checking login information such as usernames and passwords. It compares this information with a secure database in Active Directory to determine if the user has access to the system.
  
#### Tool mimikatz

##### The way to work

- Mimikatz is a popular tool used in exploiting security holes and simulated attacks in Windows environments. Mimikatz often uses techniques like injection and hooking to attack LSASS authentication and obtain sensitive credentials such as user passwords.
- Specifically, Mimikatz can use DLL injection technique to inject a custom dynamic library (DLL) into the LSASS process. This allows Mimikatz to track and record credentials when a user enters a password into the system. The injection technique allows Mimikatz to interfere with the LSASS flow and collect sensitive information.

##### Demo

- We will use two command.
  ```bash
  privilege::debug
  token::elevate
  ```
  - Command "privilege::debug": This is a command in Mimikatz to give debug privileges to a running process. Debug permissions allow a process to gain access to sensitive information, including reading or writing to the memory of other processes.
    - Providing debugging permissions can allow Mimikatz to perform operations such as reading passwords or sensitive information from authentication processes such as LSASS. However, to execute this command, users often need higher permissions, even Administrator rights.
  - Command "token::elevate": This is the command in Mimikatz to augment the token (elevate token) of the running process. A token is a mechanism in the Windows operating system to represent the authority of a user or process.
    - When executing the "token::elevate" command, Mimikatz tries to create a token with a higher authority than the current token. This can allow Mimikatz to perform operations with greater authority, including accessing sensitive information and performing system management actions.
  ![Picture](../19.%20Password%20Attacks/Image/17.png)
- Now we can use lsadump::sam to dump the contents of the SAM database.
  ![Picture](../19.%20Password%20Attacks/Image/18.png)

### Passing the Hash in Windows

#### Technique Pass the Hash

- The mechanism of operation of the Pass-the-Hash (PtH) technique is based on the use of NTLM/LM hashes for authentication and access to the target system. Here are the basic steps in the PtH process:
  - Collect NTLM/LM hash: The attacker obtains the NTLM/LM hash from the target computer. This can be done through exploiting vulnerabilities, gathering from leaked databases, or otherwise.
  - Sending hash value over SMB protocol: An attacker uses a PtH tool like pth-winexe to send an NTLM/LM hash over the SMB protocol to the target computer.
  - Authenticate with NTLM/LM hash: The target computer processes the received NTLM/LM hash and uses it to authenticate the user. Instead of asking for an explicit password, the target computer compares the received hash with the stored hash. If the two hashes match, authentication is successful and access is granted to the attacker.
  - Access to the target system: After successful authentication, an attacker gains access to the target system and performs arbitrary operations, including remote command execution, information gathering, migration, and more. intranet transfers, and many other actions.
- PtH's mechanism of action is based on the use of NTLM/LM hashes for authentication, as long as the target computers can accept this authentication method.

### Password Cracking

- The process of password cracking is fairly straight-forward at a high level. Once we have discovered the hashing mechanism we are dealing with in the target authentication process, we can iterate over each word in a wordlist and generate the respective message digest. 
- If the computed hash matches the one obtained from the target system, we have obtained the matching plain-text password. This is usually all accomplished with the help of a specialized password cracking program.
- Running john in pure brute force mode.We attack NT hashes (--format=NT) that we dumped using mimikatz.
  ```bash
  cat hash1.txt
  john --rules --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt --format=NT
  ```
  ![Picture](../19.%20Password%20Attacks/Image/19.png)