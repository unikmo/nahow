# NAHOW e.V. — static website rebuild (design preview)

**Status:** Design/source preview only. **Not deployed**. Existing HostEurope website untouched.

## Content and imagery
- Copy from existing NAHOW public pages: history, projects, team names, donations and legal contact.
- Do not use AI-generated or stock imagery.
- `assets/images/` is deliberately empty until the original photos are obtained from the existing WordPress media library or HostEurope backup.
- Run `python tools/import-originals.py /path/to/wp-content/uploads` to copy the files byte-for-byte and generate SHA-256 inventory, then `python tools/build.py` to include photos in the design. The importer does **not** resize, re-encode, crop or otherwise edit photographs. It will also include thumbnail files already present in WordPress; they are copied unchanged. Choose hero/photo order from originals before release.
- Existing reports should be imported to the static site before decommissioning WordPress. Current outgoing report links still point to the old domain.

## Local preview
`python tools/build.py && python tools/verify.py && python -m http.server 8000` then open `http://localhost:8000`.

## Deploy plan (GitHub → HostEurope; no Vercel)
1. Back up the entire HostEurope webroot, WordPress database, uploads, and current `.htaccess`.
2. Verify domain webroot, SFTP access and SSH/FTPS availability. Confirm whether the WordPress install shares that webroot.
3. Retrieve original photos and documents, verify image hashes, check photo ordering and legal information.
4. Obtain full-site design approval and prepare separate non-production HostEurope preview directory/subdomain.
5. Test responsive layout, images, navigation, accessibility, SEO, privacy and redirects.
6. After explicit release approval, configure GitHub Actions with SFTP host/user/path and a repository secret. Deploy an atomic static release without deleting mailbox directories or unrelated hosting files. Never store secrets in Git.
7. Keep a rollback snapshot and test the live domain post-release.

## Known release blockers
- Original photos are not yet accessible for extraction. No existing image was changed.
- No HostEurope SFTP/hosting access is connected.
- Existing WordPress URL/asset mapping and reports have not been fully migrated.
- Legal data and hosting privacy details require verification.
- Production release not approved and not attempted.
