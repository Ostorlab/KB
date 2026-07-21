### Immediate Mitigation

- **Remove the hardcoded `chpasswd` line.** Inject the root password at runtime via a Docker secret, a mounted
  file, or an environment variable resolved in the entrypoint — never bake it into an image layer.
- **Revert `PermitRootLogin yes`** back to `PermitRootLogin no` (or `prohibit-password`) and use key-based
  authentication for any administrative access.
- **Treat the committed password as compromised** and rotate it wherever it may have been reused, including
  CI/CD variables, vaults, and any sibling images that copied the same line.
- **Purge the secret from history** (e.g. with `git filter-repo` or BFG) if the repository is shared, since
  simply deleting the line in a later commit does not remove the credential from older refs.

### Permanent Fix

Remove the OpenSSH stack from the image entirely when sshd is not required by the runtime role (a guacd-style
gateway, for example, only needs the proxy libraries — its default `CMD` does not start sshd):

```dockerfile
# Do NOT install openssh-server unless the runtime role actually requires it.
RUN apt-get update && apt-get install -y --no-install-recommends <runtime-packages-only>
```

If administrative SSH access is genuinely required, do not hardcode credentials and do not enable root password
login. Build a non-root administrative user and authorize it through a mounted key:

```dockerfile
RUN apt-get update && apt-get install -y openssh-server
RUN sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
RUN sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
RUN useradd -m -s /bin/bash admin && mkdir -p /home/admin/.ssh && chmod 700 /home/admin/.ssh
# AuthorizedKeysFile is supplied via a mounted secret; never baked into the image.
```

Then move sshd startup (if still needed) into a controlled entrypoint and document the runtime condition so it is
not silently enabled:

```dockerfile
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```sh
#!/bin/sh
# entrypoint.sh - starts the runtime process; optionally starts sshd only when explicitly requested.
if [ "${ENABLE_SSHD:-0}" = "1" ]; then
  mkdir -p /var/run/sshd
  /usr/sbin/sshd
fi
exec guacd -f -b 0.0.0.0 -l 4822
```

### Hardening Checklist

- Prefer multi-stage builds and a distroless/minimal base so the OpenSSH server is not present at all.
- Never use `echo 'user:pass' | chpasswd` in a Dockerfile; treat any credential in a build file as a finding.
- Bind sshd to the internal container network only and never publish port 22 on the host.
- Scan Dockerfiles in CI for `chpasswd`, `PermitRootLogin yes`, and other credential/root-login patterns before
  images are built and pushed.

### Verification

- `grep -n 'chpasswd\|PermitRootLogin' Dockerfile` returns no hardcoded password and `PermitRootLogin no`.
- Build the image and confirm `ssh root@<host>` is refused with the old credential.
- Confirm the credential does not appear in any image layer (`docker history --no-trunc <image>`).
