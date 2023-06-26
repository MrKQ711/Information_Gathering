# Content

- [Content](#content)
  - [Introduction to the x86 Architecture](#introduction-to-the-x86-architecture)
    - [Program Memory](#program-memory)
      - [The Stack](#the-stack)
      - [Function Return Mechanics](#function-return-mechanics)
    - [CPU Registers](#cpu-registers)
      - [General Purpose Registers](#general-purpose-registers)
      - [ESP - The Stack Pointer](#esp---the-stack-pointer)
      - [EBP - The Base Pointer](#ebp---the-base-pointer)
      - [EIP - The Instruction Pointer](#eip---the-instruction-pointer)
  - [Buffer Overflow Walkthrough](#buffer-overflow-walkthrough)
    - [Sample Vulnerable Code](#sample-vulnerable-code)
    - [Introducing the Immunity Debugger](#introducing-the-immunity-debugger)
      - [The way to work](#the-way-to-work)
  
## Introduction to the x86 Architecture

### Program Memory

- Example of a program memory layout.
  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/1.png)
  - Code area is an area of memory in a program that contains computer code that is translated and stored in binary format for execution.
  - The Data area contains local variables, global variables, and constants used in the program.
  - Heap area and Stack area are two parts of memory used during the running of a program.
    - Heap area: This is an area of memory that is dynamically allocated during the execution of the program.
    - Stack area: This is the memory area used to store the values of local variables and information related to the calling function during the execution of the program.
- Between different memory areas during the program's execution there may exist an area of unallocated memory (Unallocated Memory), also known as a hole or a gap. This memory area is the result of allocating memory in units larger than the required size of the variables or objects and leaving spaces between them.

#### The Stack

- While a thread is running, it executes code from within the Visualization Program or from various Dynamic Link Libraries (DLLs). Threads require a short-term data area to hold functions, local variables, and program control information, called the stack. To facilitate independent execution of multiple threads, each thread in a running application has its own stack. Stack memory is viewed by the CPU as a Last-In-First-Out (LIFO) structure. This means that while accessing the stack, the elements inserted ("pushed") on the top of the stack will be removed ("popped") first. The x86 architecture implements separate PUSH and POP assembly instructions to add or remove data from the stack.

#### Function Return Mechanics

- When a program calls a function, it needs to know the address to return to after completing the execution of the function. This address is stored in stack memory along with other information related to the function's execution, such as local variables and parameters.
- Each function can have multiple stack frames corresponding to each function call. When the function terminates, the return address will be removed from the stack frame and the CPU will return to that location to continue executing the program.
  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/2.png)

### CPU Registers

- We can think of registers in the CPU as a scrap of paper (scratchpad) that stores temporary values that the CPU needs to use to perform computation and data processing operations. These values are not permanently stored and have meaning only within the execution scope of the program.
- However, the value stored in registers has a very fast access speed, so they are often used to optimize program performance. When values need to be stored permanently, they are stored in internal memory (RAM) or other storage devices on the computer.
- Register names were established for 16-bit architectures and were later extended with the advent of 32-bit (x86) platforms, hence the letter "E" appearing in the abbreviations of the registers. take note. Each register can contain a 32-bit value (values from 0 to 0xFFFFFFFF are allowed) or it can hold a 16-bit or 8-bit value in the respective subregisters as shown in the register.
  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/3.png)
  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/4.png)

#### General Purpose Registers

- Several registers, including EAX, EBX, ECX, EDX, ESI, and EDI are often-used as general purpose registers to store temporary data. 
- There is some primary registers :
  - EAX (accumulator): Arithmetical and logical instructions.
  - EBX (base): Base pointer for memory addresses.
  - ECX (counter): Loop, shift, and rotation counter.
  - EDX (data): I/O port addressing, multiplication, and division.
  - ESI (source index): Pointer addressing of data and source in string copy operations.
  - EDI (destination index): Pointer addressing of data and destination in string copy operations.

#### ESP - The Stack Pointer

- The pointer ESP (Extended Stack Pointer) is used to access values in the stack by changing its address to point to different elements in the stack.
- When a value is pushed onto the stack, the ESP pointer is decremented by the size of that value to point to the newest position on the stack. Similarly, when a value is popped off the stack, the ESP pointer will grow by an amount equal to the size of that value to point to the next position on the stack.

#### EBP - The Base Pointer

- During the execution of a thread, it can become difficult for a 
function to locate its own stack frame, which stores the required arguments, local variables, and the return address. 
EBP, the base pointer, solves this by storing a pointer to the top of the stack when a function is called. By accessing EBP, a function can easily reference information from its own stack frame (via offsets) while executing.
- Example
  ```cpp
  void foo(int a, int b, int c) {
    int sum = a + b + c;
    printf("Sum is %d", sum);
  }

  int main() {
    foo(1, 2, 3);
    return 0;
  }
  ```
  - In the above example, the function foo takes three integer arguments a, b, and c. The function will calculate the sum of these values and print the result. When function foo is called from within main, the EBP pointer in main's stack frame is backed up and updated to point to the top of foo's stack frame.
  - Then, when foo accesses arguments a, b, and c, it uses EBP to access their offsets on the stack frame.
  - For example, to access a, b, and c, foo can use offsets -8(%ebp), -12(%ebp) and -16(%ebp) corresponding to the arguments on the stack frame.
  - Finally, when foo finishes executing and returns to main, the EBP pointer will be updated to point to the top of main's stack frame and foo's stack frame will be released.

#### EIP - The Instruction Pointer

- The instruction pointer, is one of the most important registers for our purposes as it always points to the next code instruction to be executed.
- Since EIP essentially directs the flow of a program, it is an attacker’s primary target when exploiting any memory corruption vulnerability 
such as a buffer overflow.
- Example
  ```cpp
  section .data
    msg db "Hello, World!", 0 ; string

  section .text
    global _start

  _start:
    ; put the address of msg to EIP
    mov eax, msg
    mov ebx, 1
    mov ecx, eax
    mov edx, 13
    int 0x80 ; syscall write()

    ; exit the program
    mov eax, 1
    xor ebx, ebx
    int 0x80 ; syscall exit()
  ```
  - In the above example, the value of the EIP register is determined by the mov eax, msg instruction and will be used to output the string "Hello, World!" out the screen. After executing this instruction, the CPU will update the value of the EIP register to point to the next instruction in the program.

## Buffer Overflow Walkthrough

### Sample Vulnerable Code

  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/5.png)
  - The above code has a buffer overflow vulnerability, which occurs when the path entered into the program is longer than 63 characters. In this case, the strcpy() function will copy the entire path into the 64-byte buffer and cause the memory area after the buffer to overflow. This can cause unexpected errors or remote attacks such as executing malicious code or resetting the values of other variables in the program.
  ![Picture](../10.%20Introduction%20to%20Buffer%20Overflows/Image/6.png)

### Introducing the Immunity Debugger

#### The way to work

- Immunity Debugger is a powerful new way to write exploits, analyze malware, and reverse engineer binary files. It builds on a solid user interface with function graphing, the industry's first heap analysis tool built specifically for heap creation, and a large and well supported Python API for easy extensibility.
- Immunity Debugger monitors program activity using "hooking" techniques. Hooking is a technique that allows a program to change or extend the behavior of another program as it is executed. Specifically, Immunity Debugger will inject some code into the program's execution to log its activities.
- Immunity Debugger uses hooking techniques to monitor system calls, function calls inside dynamic libraries, and function calls within the program itself. It can also log events such as requests for network resources, read and write files, etc.
- When the Immunity Debugger detects an important event, it creates logs to store information about program activity. This record includes information such as the address of the function being called, the values of the registers, notes about the operation, and other relevant information.