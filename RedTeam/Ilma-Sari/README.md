# Ilma Sari — Red Team Assessment

Dokumentasi hasil **Penetration Testing dan Vulnerability Assessment** sebagai bagian dari **Proyek Akhir Keamanan Siber**.

Assessment dilakukan untuk mengidentifikasi potensi kerentanan, kesalahan konfigurasi, serta informasi sensitif yang dapat terekspos pada aplikasi web yang menjadi target pengujian.

---

## Identitas

**Nama:** Ilma Sari  
**Tim:** Red Team  
**Project:** Proyek Akhir Keamanan Siber

---

## Tujuan Assessment

Assessment ini bertujuan untuk:

- Mengidentifikasi vulnerability pada aplikasi web.
- Mengidentifikasi konfigurasi atau file sensitif yang dapat diakses secara publik.
- Melakukan validasi terhadap temuan menggunakan evidence teknis.
- Menilai dampak dan tingkat risiko dari setiap temuan.
- Memberikan rekomendasi remediation kepada pihak pengelola sistem.
- Mendokumentasikan hasil pengujian dalam bentuk laporan dan screenshot evidence.

---

## Target Pengujian

Assessment mencakup dua target:

### 1. PPSDM BMKG

`https://ppsdm.bmkg.go.id/`

Temuan utama:

- Public exposure `.claude/settings.json`
- Public exposure `.claude/settings.local.json`
- Exposure konfigurasi internal
- Exposure credential database pada konfigurasi
- Missing/incomplete security headers
- Cookie security policy
- Missing Subresource Integrity (SRI)

### 2. STAMAR Merak BMKG

`https://stamar-merak.bmkg.go.id/`

Temuan utama:

- Public exposure `/wp-content/backup-db/`
- Directory listing aktif
- Database backup dapat terdaftar secara publik
- Backup archive dapat terdaftar secara publik
- Potential exposure `.env` backup
- Exposure `phpinfo.php`
- Exposure `server-status`
- Exposure administrative resources seperti `phpmyadmin/`

---

## Tools

Tools yang digunakan dalam assessment antara lain:

- **Nuclei v3.11.1**
- **Nuclei Templates v10.4.8**
- **curl**
- Browser untuk validasi dan dokumentasi evidence

Nuclei digunakan untuk melakukan automated vulnerability dan misconfiguration detection, sedangkan `curl` digunakan untuk melakukan validasi manual terhadap endpoint yang terdeteksi.

---

## Ringkasan Temuan

| ID | Target | Temuan | Severity |
|---|---|---|---|
| VA-01 | PPSDM BMKG | Public Exposure `.claude` Configuration | Critical |
| VA-02 | PPSDM BMKG | Database Credential Exposure | Critical |
| VA-03 | PPSDM BMKG | Missing / Incomplete Security Headers | Low–Medium |
| VA-04 | PPSDM BMKG | Cookie SameSite Policy | Low |
| VA-05 | PPSDM BMKG | Missing Subresource Integrity | Low |
| VA-06 | STAMAR Merak | Public Backup Directory Exposure | Critical |

---

## Temuan Prioritas Tinggi

### VA-01 & VA-02 — PPSDM BMKG

Endpoint konfigurasi berikut terdeteksi dapat diakses melalui HTTP:

```text
/.claude/settings.json
/.claude/settings.local.json
