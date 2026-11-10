# Security policy

## Supported material

This repository contains original font sources, build and validation scripts, artwork, documentation, and downloadable Vantablack Gothic 0.1.0 alpha binaries. Only the latest alpha on main is maintained. No tagged stable release or response-time guarantee is claimed.

## Reporting a vulnerability

Do not publish exploit details, credentials, private documents, or malicious font files in public issues.

If GitHub shows **Report a vulnerability** under this repository's Security tab, use that private reporting flow. Private vulnerability reporting is not asserted to be enabled by this document. If that option is unavailable, open a minimal public issue asking the maintainer to arrange a private reporting channel, without describing the vulnerability, attaching a payload, or identifying affected private systems.

Once a private channel is arranged, include the affected commit, environment, impact, minimal reproduction, and suggested remediation. Keep a report private while a fix and disclosure are coordinated.

## Scope

Report unsafe build scripts, dependency compromise, unintended file access, malicious source processing, and font-generation or specimen code vulnerabilities. Ordinary glyph requests, readability problems, missing coverage, and rendering differences belong in normal issue templates unless they have a concrete security impact.

## Contributor expectations

Do not commit credentials, execute untrusted source contributions without inspection, or redistribute malicious binaries. Future dependency and font parsing work must validate inputs and document supported versions.
