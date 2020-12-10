# stf20-writeups

## Reversing - Time Travel
We are given a TIMELOG.run file. This is a windows Time Travel Debugging trace, which we can open and analyse with windbg preview. By running the `lm m *` command within the trace to list the loaded modules, we can see that this is a trace of (64-bit) wordpad.exe, suggesting that we likely need to leak the typed contents.

wordpad.exe is a Windows GUI application, which means that at some level, user input should be dispatched to the application in an event loop and received by a variant of the `USER32!GetMessage` function, in our case the `USER32!GetMessageW` function. Indeed, putting a breakpoint on the method shows it getting triggered. `GetMessageW` reads the events into the `LPMSG` pointer in its first argument, which has the following structure:

```
typedef struct tagMSG {
  HWND   hwnd;
  UINT   message;
  WPARAM wParam;
  LPARAM lParam;
  DWORD  time;
  POINT  pt;
  DWORD  lPrivate;
} MSG, *PMSG, *NPMSG, *LPMSG;
```

We are interested in messages of type `WM_CHAR` (0x102), which are dispatched to the event queue after `TranslateMessage` translates virtual-key messages into characters. `wParam` contains the character code for the key and `lParam` contains the repeat count (from holding down the key) in a bitfield. Fortunately there were no repeats and we only needed to look at the `wParam` field.

Therefore we set a breakpoint near the end of `GetMessageW`, and using the pointer to the buffer saved in `rbx` read out the message type and print the character if it is an `WM_CHAR` message:

```
bp USER32!GetMessageW+0x54 ".if (poi(rbx+0x8)==0x102) {.printf \"%c\n\", poi(rbx+0x10)} .else {gc}"
```

and then repeatedly executing `g` and waiting for the breakpoint to hit eventually prints out the contents of the file character by character (including backspaces, which have to be accounted for), giving the flag `govtech-csg{Y0u_d0NT_n3eD_no_71m3$T0nE}`.


## Reversing - Striking Back 1
We are given a .NET binary that we can decompile. Some reversing indicates that it wants a 32-character string in the first argument to the executable, then it does a bunch of repeated hashing of the input before checking some bytes in the hashed result. This turns out to mostly be time-wasting and we can ignore this, as it does not use this result further.

After that, it takes the input and runs it through `func1`, `func4` and `func2` in that order twice, then does a character-by-character check on the output with a string stored in the binary, and prints out our input as the flag. These functions are not particularly interesting and just scramble the input, the only one of note is `func4`, which is implemented as a native method, which we can reverse using IDA.

All of the functions are easily invertible, and by executing their inverses in the reverse order on the string stored in the binary we can obtain the flag `govtech-csg{h0pp1ng_btwn_w0rlds}`. See the [solve script](striking-back-1-solve.py) for details.
