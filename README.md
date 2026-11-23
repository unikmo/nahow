# NAHOW e.V. — website rebuild

**Status: live on https://nahow.de since 2026-11-23 (commit 0a054b4 deployed to HostEurope `/public_html`).** Original photographs and report PDFs are included unchanged (see `assets/*/ORIGINALS-MANIFEST.json`).

## Architecture

- Static German website; no database or Vercel required.
- GitHub → GitHub Actions → HostEurope via explicit FTPS on port 21.
- FTPS server: `ftp.nahow.de`; deployment username: `nahow@nahow.de`.
- Real web root: `/home/duy6zx6o0x4d/public_html` (cPanel primary domain). Other domains live in subfolders of it: never mirror-delete there. The `.htaccess` is scoped to nahow.de for that reason.
- Do not commit FTPS credentials. Store them only in repository Actions secrets after authentication is available.

## Non-negotiable content preservation

- All original project photographs remain unchanged (no re-encoding, cropping, AI replacement, or substitution).
- Back up WordPress webroot, uploaded media, database, report PDFs, and `.htaccess` before switching.
- Verify donation details, legal information, redirects, photo mapping, responsive design, navigation, and rollback.
- Do **not** deploy a photograph-free version to production.

## Source status

Deployed. Old WordPress files are in the hosting account's cPanel Trash; a zip of the old files is in `/home/duy6zx6o0x4d/application_backups/`. The WordPress database was left in place. Legal review of the Impressum and Datenschutz (section III) by the association is still open.
