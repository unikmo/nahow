# NAHOW e.V. — website rebuild

**Status: preview source committed on `preview/website-rebuild`; not deployed.** Existing `nahow.de` remains hosted at HostEurope.

## Architecture

- Static German website; no database or Vercel required.
- GitHub → GitHub Actions → HostEurope via explicit FTPS on port 21.
- FTPS server: `ftp.nahow.de`; deployment username: `nahow@nahow.de`.
- HostEurope target path (verify FTP-relative mapping before deployment): `/home/duy6zx6o0x4d/public_html/nahow.de/nahow`.
- Do not commit FTPS credentials. Store them only in repository Actions secrets after authentication is available.

## Non-negotiable content preservation

- All original project photographs remain unchanged (no re-encoding, cropping, AI replacement, or substitution).
- Back up WordPress webroot, uploaded media, database, report PDFs, and `.htaccess` before switching.
- Verify donation details, legal information, redirects, photo mapping, responsive design, navigation, and rollback.
- Do **not** deploy a photograph-free version to production.

## Source status

The website source, build and verification scripts are committed to this preview branch. The original photographs and project documents remain unimported. Production deployment is disabled pending secure HostEurope access, full backup, photo/report migration, visual review, and release verification.
