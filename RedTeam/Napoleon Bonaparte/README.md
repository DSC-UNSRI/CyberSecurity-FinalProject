# Web Security Assessment — Red Team Final Project

Laporan hasil pengujian keamanan aplikasi web pada dua target program CSIRT/VDP resmi, dilakukan sebagai proyek akhir Red Team (Cybersecurity).

## 🎯 Tujuan

Menguji dan mengevaluasi tingkat keamanan aplikasi web pada target yang tercakup dalam program CSIRT/VDP (Vulnerability Disclosure Program) resmi, guna mengidentifikasi celah keamanan yang berpotensi dieksploitasi pihak tidak bertanggung jawab. Pengujian dilakukan melalui pendekatan Red Team secara etis (*ethical hacking*), dan hasil temuan digunakan sebagai dasar rekomendasi perbaikan bagi pengelola sistem.

## 🌐 Target

| Target | Program VDP | IP / Server |
|---|---|---|
| `*.bmkg.go.id` | [CSIRT BMKG](https://csirt.bmkg.go.id/page/vdp) | NS1/NS2/NS3.BMKG.GO.ID · `104.20.20.136`, `172.66.159.70` |
| `*.kukarkab.go.id` | [VDP Etam Kukarkab](https://ttis.kukarkab.go.id/page/vdp-etam) | ns1–ns4.rumahweb.com/net · `103.97.202.82` |

## 🚫 Batasan Pengujian

Pengujian **tidak boleh** bersifat destruktif. Temuan hanya dieksploitasi sebatas *Proof of Concept* (PoC). Tindakan berikut **dilarang** dan mengakibatkan diskualifikasi:

- Server/Web Defacement
- Domain Takeover / DNS Hijacking
- Data Wiping / Modification
- Denial of Service (DoS/DDoS)
- Social Engineering / Phishing

## 🧭 Metodologi

1. **Reconnaissance (Information Gathering)** — subdomain enumeration, port scanning, OSINT (pasif & aktif)
2. **Vulnerability Analysis** — pemetaan permukaan aplikasi & input vector
3. **Exploitation** — pembuktian kerentanan via *safe exploitation* untuk menyusun PoC tanpa merusak data target
4. **Post-Exploitation** — sangat dibatasi, hanya untuk membuktikan besaran dampak (impact analysis)
5. **Reporting** — dokumentasi teknis sesuai standar industri

## 🔍 Findings Summary

| No | Temuan | Target | Severity | CVSS | CWE | Confidence |
|---|---|---|---|---|---|---|
| 1 | CSP: Failure to Define Directives with No Fallback | `bmkg.go.id` | 🟠 Medium | 4.3 | CWE-693 | High |
| 2 | Cookie Without a Secured Flag | `*.kukarkab.go.id` | 🟡 Low | 2.6 | CWE-614 | Medium |

Tidak ditemukan kerentanan Critical/High. Kedua temuan bersifat kelemahan konfigurasi (security header & atribut cookie), bukan kerentanan struktural aplikasi (seperti SQLi, RCE, atau Broken Access Control).

### 1. CSP: Failure to Define Directives with No Fallback — `bmkg.go.id`

**Deskripsi:** Header `Content-Security-Policy` tidak mendefinisikan directive `frame-ancestors` dan `form-action` secara eksplisit. Kedua directive ini tidak mengikuti fallback `default-src`, sehingga situs tetap berisiko disematkan ke `<iframe>` pihak lain dan form dapat diarahkan ke server luar.

**Dampak:** Risiko *Clickjacking* dan *Form Redirection/Hijacking*.

**Deteksi otomatis (OWASP ZAP):**

<!-- 📸 Taruh screenshot hasil scan OWASP ZAP untuk temuan CSP di sini -->
`[ screenshot: zap-csp-scan.png ]`

**Deteksi manual (`curl -m 10 -i https://www.bmkg.go.id/cuaca/radar`):**

<!-- 📸 Taruh screenshot output curl / response header di sini -->
`[ screenshot: curl-csp-header.png ]`

**Remediation:**
```
Content-Security-Policy: ...; frame-ancestors 'self'; form-action 'self';
```

---

### 2. Cookie Without a Secured Flag — `*.kukarkab.go.id`

**Deskripsi:** Cookie `cookiesession1` dikirim tanpa atribut `Secure`, sehingga tetap disertakan browser meski diakses melalui HTTP (tidak terenkripsi), dan berisiko dicuri lewat serangan *Man-in-the-Middle*.

**Dampak:** *Session Sniffing/MitM* dan *Session Hijacking*.

**Deteksi otomatis (OWASP ZAP):**

<!-- 📸 Taruh screenshot hasil scan OWASP ZAP untuk temuan cookie di sini -->
`[ screenshot: zap-cookie-scan.png ]`

**Deteksi manual (response header `Set-Cookie`):**

<!-- 📸 Taruh screenshot bukti header Set-Cookie tanpa flag Secure di sini -->
`[ screenshot: manual-cookie-header.png ]`

**Remediation:**
```
Set-Cookie: cookiesession1=value; Secure; HttpOnly; SameSite=Lax
```

## 🛠️ Rekomendasi & Mitigasi

**1. Perbaikan spesifik**
- `bmkg.go.id`: tambahkan directive `frame-ancestors` dan `form-action` pada header CSP
- `*.kukarkab.go.id`: tambahkan atribut `Secure`, `HttpOnly`, `SameSite` pada cookie sesi, serta paksa redirect HTTP → HTTPS di seluruh domain

**2. Rekomendasi umum (hardening)**
- Terapkan security header tambahan secara menyeluruh: `Strict-Transport-Security` (HSTS), `X-Content-Type-Options: nosniff`, `X-Frame-Options`, `Referrer-Policy`
- Lakukan pengujian keamanan (VA/PT) secara berkala, bukan hanya sekali
- Monitoring & logging traffic mencurigakan (mis. percobaan akses HTTP pada domain yang seharusnya HTTPS-only)
- Security awareness training untuk tim developer terkait konfigurasi header & cookie yang aman

## 🧰 Tools

| Tool | Fungsi |
|---|---|
| Nikto | Vulnerability scanner |
| dirb | Scanning confidential directories |
| OWASP ZAP | Vulnerability scanner |
| cURL | Manual validating |

## 📄 Laporan Lengkap

Lihat [`Napoleon_Bonaparte_CS_FINAL_PROJECT.docx`](./Napoleon_Bonaparte_CS_FINAL_PROJECT.docx) untuk parameter vector CVSS lengkap, analisis teknis, dan bukti deteksi setiap temuan.

## 👤 Author

**Napoleon Bonaparte** — Cybersecurity, Red Team

## ⚠️ Disclaimer

Pengujian dilakukan secara legal dalam lingkup program VDP resmi masing-masing instansi. Seluruh temuan dilaporkan secara *responsible disclosure* dan tidak dimaksudkan untuk disalahgunakan.
