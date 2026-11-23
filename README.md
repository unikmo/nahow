# NAHOW e.V. — website rebuild

**Status: preview package prepared; not deployed.** Existing `nahow.de` remains hosted at HostEurope.

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

The preview ZIP exists as a conversation artifact but has **not** been committed to this repository yet. Do not run automated deployment from this branch. The complete source must be transferred into this repository, tested, and reviewed before release.
