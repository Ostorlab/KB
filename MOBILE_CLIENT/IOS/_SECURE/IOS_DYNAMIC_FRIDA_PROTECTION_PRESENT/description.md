The application detected and responded to Frida-based dynamic instrumentation on iOS.

This indicates that the application includes runtime resilience controls intended to identify instrumentation through Frida or Frida Gadget and to react when those conditions are observed. In practice, this can raise attacker cost by making runtime observation, hook-based bypasses, and live tampering more difficult.

This result is informative rather than absolute. Frida detection can improve resilience, but it does not guarantee resistance to all runtime tampering techniques, custom instrumentation builds, or bypasses. High-value trust decisions should still be enforced server-side.
