`RELRO`: RELRO is a memory protection technique to harden against memory corruption exploitation techniques. RELRO prevents GOT overwrite attacks.

`ASLR`: ASLR is a memory protection technique to harden against memory corruption exploitation technique. ASLR randomizes the address space of binary to prevent controlled address jumps.

`No eXecute`: Mark memory region as non-executable to harden against memory corruption exploitation technique.

`Stack canary`: Add a canary to memory that gets overwritten in the case of a memory corruption. The canary is checked at runtime to prevent the exploitation of the memory corruption vulnerability.