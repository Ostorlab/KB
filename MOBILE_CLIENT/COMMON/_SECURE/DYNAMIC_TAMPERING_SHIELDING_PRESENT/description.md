The application implements shielding against dynamic tampering.
It crashes or behaves abnormally in presence of a dynamic instrumentation tools.

**Definition:** Dynamic tampering refers to the manipulation of an application during runtime, typically using debugging or hooking tools to alter its behavior without modifying its code.

**Common attacks:**

- **Function Hooking:** Intercepting function calls to modify arguments, return values, or replace in-memory implementations entirely.
- **In-Memory Manipulation:** Directly reading or altering memory contents at runtime to bypass logic or extract sensitive data.
- **Parameter Tampering:** Intercepting and modifying data exchanged between components, layers, or services during execution.
- **Environment & Logic Tampering:** Altering environment variables, configuration values, or control flow to subvert intended application behavior.