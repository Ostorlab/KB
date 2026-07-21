A root (or administrative) SSH password is committed in plaintext inside a Dockerfile, and `PermitRootLogin yes` is
explicitly set in the same image, overriding the Debian default (`PermitRootLogin without-password` /
`prohibit-password`). Because the credential lives in source control, anyone with repository read access holds the
root credential of every image built from that Dockerfile.

The vulnerable pattern looks like:

```dockerfile
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:fightlikeachamp$$1' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
EXPOSE 22
```

Two distinct weaknesses are combined in the same build:

1. **Hard-coded credential (CWE-798 / CWE-522):** the `chpasswd` line bakes a known password into the image layers.
   The value is recoverable from the resulting image and from the repository history, so it cannot be considered
   secret. Shell escaping (`$$` -> `$`) further misleads operators about the effective password value.
2. **Improper privilege management (CWE-269):** `PermitRootLogin yes` re-enables direct password-based root login
   over SSH even when the base image ships a safer default, defeating key-based-only authentication policies.

### Security Impact

- **Credential disclosure:** repository readers, CI logs, and image-layer inspectors all recover the plaintext
  root password. Rotation is impossible without rebuilding the image and rotating the value everywhere it was reused.
- **Root host access:** when `sshd` is started (via an overridden `CMD`, an entrypoint, or a manual
  `service ssh start`) and port 22 is reachable, the committed password yields a direct root shell on the
  container host.
- **Lateral movement:** a root shell on a gateway/proxy host (e.g. a guacd-style jump host) lets an attacker
  inspect and tamper with proxied backend credentials in transit, abuse locally-installed tooling, and pivot to
  every internal service the container can reach.
- **Conditionality:** this finding is configuration-proven but runtime-conditional. When the default `CMD` only
  starts the application (e.g. `guacd`) and does not start `sshd`, exploitation additionally requires sshd to be
  running and port 22 to be reachable. This is why the issue is rated Medium rather than High.
