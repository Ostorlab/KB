Avoiding memory leaks in applications is difficult. There are tools with
aide in tracking down such memory leaks like Valgrind or using modern compiler tools like `ASAN`, `MSAN` and `UBSAN`.

Valgrind runs the desired program in an environment such that all memory allocation and de-allocation routines are
checked. At the end of program execution, Valgrind will display the results in an easy-to-read manner.