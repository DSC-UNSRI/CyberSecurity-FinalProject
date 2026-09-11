# Ilma Sari — Red Team Assessment

Dokumentasi hasil **Penetration Testing / Vulnerability Assessment** untuk Final Project Cyber Security.

> **Author:** Ilma Sari  
> **Team:** Red Team  
> **Assessment Type:** Penetration Testing / Vulnerability Assessment  
> **Tools:** Nuclei v3.11.1, curl, browser  
> **Status:** Assessment & validation evidence

---

## 1. Overview

Assessment ini mendokumentasikan hasil pengujian keamanan terhadap:

- `https://ppsdm.bmkg.go.id/`
- `https://stamar-merak.bmkg.go.id/`

Pengujian dilakukan menggunakan kombinasi **automated vulnerability scanning** dengan Nuclei dan **manual validation** menggunakan `curl`.

Fokus assessment meliputi:

1. Exposure file konfigurasi.
2. Exposure credential/database configuration.
3. HTTP security header hardening.
4. Cookie security.
5. Subresource Integrity (SRI).
6. Public backup directory / directory listing.

---

## 2. Scope

| Target | Aktivitas |
|---|---|
| `ppsdm.bmkg.go.id` | Nuclei scanning dan validasi exposure konfigurasi |
| `stamar-merak.bmkg.go.id` | Nuclei scanning dan validasi backup directory |

### Metodologi

```text
Reconnaissance
      ↓
Technology / Endpoint Detection
      ↓
Nuclei Automated Scanning
      ↓
Manual Validation
      ↓
Evidence Collection
      ↓
Risk & CVSS Assessment
      ↓
Remediation Recommendation
```

---

## 3. Executive Summary

Hasil assessment menunjukkan beberapa kelemahan keamanan yang perlu mendapatkan perhatian, terutama pada **exposure konfigurasi dan artefak sensitif melalui web**.

Temuan dengan prioritas tertinggi adalah:

- Exposure konfigurasi `.claude` pada PPSDM.
- Indikasi credential database di dalam konfigurasi yang dapat diakses publik.
- Public directory listing pada lokasi backup STAMAR Merak.

Temuan hardening lainnya meliputi konfigurasi security header, cookie `SameSite`, dan penggunaan Subresource Integrity.

> **Catatan:** Evidence yang tersedia menunjukkan exposure informasi. Credential yang terlihat pada screenshot **tidak digunakan untuk melakukan login, akses database, perubahan data, atau destructive action** dalam assessment ini.

---

## 4. Findings Summary

| ID | Target | Finding | CWE | CVSS | Severity |
|---|---|---|---|---:|---|
| 5.1 | PPSDM | Public Exposure of `.claude` Configuration Files | CWE-200 | 7.5 | 🔴 High |
| 5.2 | PPSDM | Exposure of Database Credentials in Public Configuration | CWE-798 | 9.8* | 🔴 Critical |
| 5.3 | PPSDM | Missing / Incomplete HTTP Security Headers | CWE-693 | 4.3 | 🟠 Medium |
| 5.4 | PPSDM | Cookie SameSite Policy Not Strictly Configured | CWE-1275 | 4.3 | 🟠 Medium |
| 5.5 | PPSDM | Missing Subresource Integrity (SRI) | CWE-829 | 3.7 | 🟢 Low |
| 5.6 | STAMAR Merak | Public Backup Directory Exposure | CWE-548 | 7.5 | 🔴 High |

\* Skor 9.8 merepresentasikan skenario apabila credential yang terekspos masih aktif dan memiliki privilege tinggi. Validitas credential tidak diuji dalam assessment ini.

---

# 5. Detailed Findings

## 5.1 Public Exposure of `.claude` Configuration Files

**Judul:** Public Exposure of `.claude` Configuration Files  
**CWE:** CWE-200 — Exposure of Sensitive Information to an Unauthorized Actor  
**CVSS 3.1:** 7.5 (High)

### Deskripsi

File:

```text
/.claude/settings.json
/.claude/settings.local.json
```

terdeteksi oleh Nuclei dan dapat diakses secara langsung melalui web.

Validasi manual menunjukkan bahwa endpoint tersebut mengembalikan isi konfigurasi.

### Dampak

Exposure konfigurasi dapat mengungkap:

- Struktur internal aplikasi.
- Path source code.
- Command administratif.
- Informasi koneksi database.
- Informasi lingkungan aplikasi.
- Detail yang dapat membantu reconnaissance dan serangan lanjutan.

### POC

1. Jalankan Nuclei terhadap target PPSDM.
2. Identifikasi hasil `claude-settings-exposure`.
3. Request `/.claude/settings.json`.
4. Request `/.claude/settings.local.json`.
5. Konfirmasi bahwa server mengembalikan konfigurasi.

### Evidence

![Nuclei PPSDM](RedTeam/Evidence/01-nuclei-ppsdm.png.)

![Claude Settings](RedTeam/Evidence/02-claude-settings.png)

![Claude Settings Local](ReadTeam/Evidence/03-claude-settings-local.png)

### Rincian CVSS

- **Attack Vector:** Network
- **Attack Complexity:** Low
- **Privileges Required:** None
- **User Interaction:** None
- **Scope:** Unchanged
- **Confidentiality:** High
- **Integrity:** None
- **Availability:** None

### Rekomendasi

- Hapus `.claude/` dari web root.
- Blokir akses HTTP terhadap file konfigurasi developer.
- Audit deployment artifact.
- Tambahkan secret/configuration scanning pada CI/CD.

---

## 5.2 Exposure of Database Credentials in Public Configuration

**Judul:** Exposure of Database Credentials in Public Configuration  
**CWE:** CWE-798 — Use of Hard-coded Credentials  
**CVSS 3.1:** 9.8 (Critical)*

### Deskripsi

Validasi terhadap konfigurasi publik menunjukkan adanya command koneksi database yang memuat informasi seperti host, username, dan password.

Evidence menunjukkan penggunaan akun database dengan privilege tinggi.

Credential tersebut **tidak digunakan untuk autentikasi atau perubahan database** selama assessment.

### Dampak

Apabila credential masih aktif dan database dapat dijangkau, pihak tidak berwenang berpotensi:

- Mengakses database.
- Membaca data.
- Mengubah data.
- Menghapus data.
- Mengambil informasi sensitif.

### POC

1. Validasi `/.claude/settings.json`.
2. Identifikasi parameter koneksi database.
3. Periksa `/.claude/settings.local.json`.
4. Dokumentasikan exposure.
5. Tidak melakukan login menggunakan credential yang ditemukan.

### Evidence

![Database Credential Exposure](../Evidence/02-claude-settings.png)

![Local Configuration](../Evidence/03-claude-settings-local.png)

### Rincian CVSS

- **Attack Vector:** Network
- **Attack Complexity:** Low, jika credential masih valid
- **Privileges Required:** None
- **User Interaction:** None
- **Scope:** Unchanged
- **Confidentiality:** High
- **Integrity:** High
- **Availability:** High

### Rekomendasi

- Segera revoke/rotate credential yang terekspos.
- Hapus credential dari file yang dapat diakses publik.
- Gunakan secret manager atau environment injection.
- Terapkan prinsip least privilege.
- Batasi konektivitas database menggunakan network ACL.
- Audit database access log.

> **Security note:** Jangan menaruh password atau secret mentah di README maupun repository publik. Screenshot evidence sebaiknya di-redact sebelum di-upload.

---

## 5.3 Missing / Incomplete HTTP Security Headers

**Judul:** Missing / Incomplete HTTP Security Headers  
**CWE:** CWE-693 — Protection Mechanism Failure  
**CVSS 3.1:** 4.3 (Medium)

### Deskripsi

Nuclei mengindikasikan bahwa sejumlah security header pada PPSDM belum diterapkan atau belum dikonfigurasi secara optimal.

Security header berfungsi sebagai defense-in-depth untuk mengurangi risiko browser-side attack.

### Dampak

Ketiadaan header keamanan tidak secara langsung membuktikan compromise, tetapi dapat memperbesar dampak kerentanan lain seperti:

- Content injection.
- Clickjacking.
- MIME sniffing.
- Browser-based attack.

### POC

1. Jalankan Nuclei pada target PPSDM.
2. Identifikasi hasil terkait missing security headers.
3. Validasi HTTP response header.
4. Bandingkan dengan security baseline.

### Evidence

![Nuclei PPSDM](../Evidence/01-nuclei-ppsdm.png)

### Rekomendasi

Evaluasi dan terapkan:

- `Content-Security-Policy`
- `X-Content-Type-Options`
- `X-Frame-Options` atau `frame-ancestors`
- `Referrer-Policy`
- `Permissions-Policy`

---

## 5.4 Cookie SameSite Policy Not Strictly Configured

**Judul:** Cookie SameSite Policy Not Strictly Configured  
**CWE:** CWE-1275 — Sensitive Cookie Without `SameSite` Attribute  
**CVSS 3.1:** 4.3 (Medium)

### Deskripsi

Assessment mengindikasikan bahwa cookie aplikasi belum menggunakan konfigurasi `SameSite` yang ketat.

`SameSite` membantu membatasi pengiriman cookie dalam konteks cross-site.

### Dampak

Konfigurasi cookie yang terlalu permisif dapat meningkatkan risiko penyalahgunaan session pada skenario cross-site tertentu, terutama jika dikombinasikan dengan kelemahan lain.

### POC

1. Jalankan scanning terhadap PPSDM.
2. Identifikasi hasil cookie security.
3. Periksa response `Set-Cookie`.
4. Dokumentasikan atribut cookie.

### Evidence

![Cookie Security Evidence](../Evidence/01-nuclei-ppsdm.png)

### Rekomendasi

- Gunakan `SameSite=Lax` sebagai baseline jika sesuai.
- Gunakan `SameSite=Strict` untuk cookie yang tidak membutuhkan cross-site context.
- Terapkan `Secure` pada session cookie.
- Terapkan `HttpOnly` pada cookie yang tidak membutuhkan akses JavaScript.
- Retest login/SSO setelah perubahan.

---

## 5.5 Missing Subresource Integrity (SRI)

**Judul:** Missing Subresource Integrity (SRI)  
**CWE:** CWE-829 — Inclusion of Functionality from Untrusted Control Sphere  
**CVSS 3.1:** 3.7 (Low)

### Deskripsi

Beberapa resource JavaScript/CSS yang terdeteksi pada PPSDM tidak menggunakan Subresource Integrity.

SRI memungkinkan browser melakukan verifikasi hash terhadap resource yang dimuat.

### Dampak

Jika resource pihak ketiga mengalami perubahan tidak sah, browser dapat menerima resource tersebut tanpa validasi integrity tambahan.

### POC

1. Jalankan Nuclei terhadap PPSDM.
2. Identifikasi hasil `missing-sri`.
3. Periksa tag `<script>` atau `<link>`.
4. Konfirmasi atribut `integrity` tidak diterapkan pada resource yang relevan.

### Evidence

![Missing SRI](../Evidence/01-nuclei-ppsdm.png)

### Rekomendasi

- Tambahkan atribut `integrity`.
- Gunakan `crossorigin` sesuai kebutuhan SRI.
- Pertimbangkan self-hosting resource kritis.
- Gunakan dependency pinning.
- Tambahkan pemeriksaan integrity ke CI/CD.

---

## 5.6 Public Backup Directory Exposure

**Judul:** Public Backup Directory Exposure  
**CWE:** CWE-548 — Exposure of Information Through Directory Listing  
**CVSS 3.1:** 7.5 (High)

### Deskripsi

Pada STAMAR Merak, Nuclei mendeteksi endpoint:

```text
/wp-content/backup-db/
```

Validasi manual menunjukkan directory listing aktif dan menampilkan resource seperti:

```text
backup/
db.sql
dump.tar.gz
.env.bak
phpinfo.php
wp-login.php
phpmyadmin/
server-status
api/
```

### Dampak

Directory listing memberikan reconnaissance bernilai tinggi dan berpotensi membuka:

- Backup database.
- Archive aplikasi.
- Environment configuration.
- Informasi PHP.
- Resource administratif.
- Endpoint internal.

Evidence yang tersedia membuktikan **directory listing**, tetapi isi backup tidak diunduh atau diproses dalam assessment yang didokumentasikan.

### POC

1. Jalankan Nuclei terhadap STAMAR Merak.
2. Identifikasi temuan `wordpress-db-backup`.
3. Request:

```text
/wp-content/backup-db/
```

4. Konfirmasi directory listing.
5. Dokumentasikan nama dan metadata resource tanpa mengunduh backup/secret.

### Evidence

![Nuclei STAMAR Merak](../Evidence/04-nuclei-stamar-merak.png)

![Backup Directory Listing](../Evidence/05-backup-directory-listing.png)

### Rincian CVSS

- **Attack Vector:** Network
- **Attack Complexity:** Low
- **Privileges Required:** None
- **User Interaction:** None
- **Scope:** Unchanged
- **Confidentiality:** High
- **Integrity:** None berdasarkan evidence
- **Availability:** None berdasarkan evidence

### Rekomendasi

- Hapus backup dari web-accessible directory.
- Nonaktifkan directory indexing.
- Simpan backup pada private storage.
- Rotate secret yang pernah berada dalam backup atau `.env`.
- Batasi phpMyAdmin ke jaringan administratif.
- Batasi `server-status`.
- Review access log dan WAF log.

---

# 6. Risk Register

| Priority | Finding | Severity | Recommended Action |
|---|---|---|---|
| P1 | Database credential exposure | Critical | Revoke/rotate credential dan hapus exposure |
| P1 | `.claude` configuration exposure | High | Blokir akses publik dan hapus dari web root |
| P1 | Backup directory exposure | High | Hapus backup dari public directory |
| P2 | Security headers | Medium | Implement security header baseline |
| P2 | Cookie SameSite | Medium | Perbaiki cookie security attributes |
| P3 | Missing SRI | Low | Implement SRI/dependency integrity |

---

# 7. Remediation Priority

### P1 — Immediate

- Rotate/revoke credential yang terekspos.
- Tutup akses publik ke `.claude`.
- Hapus backup database dari web root.
- Nonaktifkan directory indexing.
- Audit access log untuk resource sensitif.

### P2 — Hardening

- Perbaiki HTTP security headers.
- Perbaiki cookie security.
- Batasi akses resource administratif.
- Audit deployment artifact.

### P3 — Preventive Control

- Implementasikan SRI.
- Gunakan dependency pinning.
- Terapkan secret scanning pada CI/CD.
- Gunakan secret manager.
- Tambahkan automated security regression testing.

---

# 8. Retest Criteria

Temuan dianggap telah diperbaiki apabila:

- `/.claude/settings.json` tidak dapat diakses publik.
- `/.claude/settings.local.json` tidak dapat diakses publik.
- Credential yang terekspos telah di-revoke/rotate.
- `/wp-content/backup-db/` tidak dapat diakses publik.
- Directory indexing telah dinonaktifkan.
- Backup dipindahkan ke private storage.
- phpMyAdmin dan server-status dibatasi.
- Security headers telah diterapkan sesuai baseline.
- Cookie menggunakan atribut keamanan yang sesuai.
- Resource eksternal kritis menggunakan SRI atau mekanisme integrity setara.

---

# 9. Evidence Directory

Screenshot disimpan pada folder:

```text
Evidence/
├── 01-nuclei-ppsdm.png
├── 02-claude-settings.png
├── 03-claude-settings-local.png
├── 04-nuclei-stamar-merak.png
└── 05-backup-directory-listing.png
```

Laporan lengkap:

```text
Laporan/
└── Laporan_Pentest_VA_Format_RedTeam_Ilma_Sari.docx
```

Struktur keseluruhan:

```text
Ilma-Sari/
├── README.md
├── Laporan/
│   └── Laporan_Pentest_VA_Format_RedTeam_Ilma_Sari.docx
└── Evidence/
    ├── 01-nuclei-ppsdm.png
    ├── 02-claude-settings.png
    ├── 03-claude-settings-local.png
    ├── 04-nuclei-stamar-merak.png
    └── 05-backup-directory-listing.png
```

---

# 10. Disclaimer

Pengujian dilakukan untuk tujuan **security assessment / educational final project** pada target yang berada dalam scope pengujian.

Assessment ini berfokus pada validasi vulnerability dan pengumpulan evidence secara terbatas. Tidak dilakukan tindakan destruktif, penghapusan data, perubahan database, maupun penyalahgunaan credential yang ditemukan.

**Sensitive information must be redacted before publication.**

---

## Author

**Ilma Sari**  
Red Team — Final Project Cyber Security
