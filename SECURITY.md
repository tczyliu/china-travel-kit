# Security policy

Please do not publish vulnerabilities, private traveler information, credentials, or precise locations of vulnerable individuals in a public issue.

Use GitHub private vulnerability reporting for sensitive reports. Include the affected version, reproduction steps, and likely impact. If private reporting is unavailable, open a public issue without sensitive details and ask the maintainer for a private channel. Maintainers should acknowledge a valid report within seven days.

Travel data corrections are normally not security vulnerabilities; use the data correction issue form unless disclosure could endanger someone.

For a suspected incomplete or modified release, first run `python3 -m china_travel_kit integrity` and include only the reported file names, not sensitive local paths or file contents. The result should report both `valid: true` and `signature_valid: true`. SHA-256 detects file changes; the Ed25519 signature authenticates the official manifest. Neither mechanism prevents copying.

The release private key must remain outside the repository. If it is lost, publish a documented public-key rotation. If it may be exposed, stop signing releases with it immediately, rotate the public key, and identify the last trusted tag.
