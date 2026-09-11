# Malware Analysis Report

> **Target OS:** Windows 10 (64-bit)  
> **Filename:** `f2413262c539ab550cdd01c88028bff17ee047d5482f0a28c03e3cc071bf4243.exe`  
> **Threat Verdict:** **Malicious** *(Score: 100/100)*  
> **Tags:** `arch-exec` | `ip-check` | `evasion`  
<img width="458" height="111" alt="Screenshot 2026-09-10 002848" src="https://github.com/user-attachments/assets/07e1a4f2-e336-4479-9e4b-e5e6f6bfc1df" />

---

## Executive Summary

Sampel dieksekusi di dalam lingkungan sandbox terisolasi dan menunjukkan rantai infeksi berlapis yang berfokus pada **persistensi ganda** dan **komunikasi berulang ke server eksternal**, alih-alih efek yang langsung terlihat oleh korban (seperti ransomware).

Pola penyebaran malware ini bertumpu pada teknik **rekayasa sosial (*social engineering*)** dengan memanipulasi psikologis calon korbannya. Penyerang sengaja mengemas berkas berbahaya ke dalam format arsip terkompresi (seperti `.zip` atau `.rar`) untuk mengelabui proteksi keamanan awal sekaligus memancing rasa penasaran pengguna.

Taktik pengiriman lampiran seperti ini biasanya menyasar dua kelompok utama:
* **Lingkungan Korporat:** Menyasar karyawan (terutama staf bagian administrasi atau keuangan) yang sudah terbiasa mengunduh dan mengekstrak dokumen kerja harian.
* **Pengguna Awam:** Memanfaatkan kelalaian pengguna biasa agar mereka langsung mengekstrak dan mengeksekusi file di dalamnya tanpa memeriksa keaslian berkas tersebut.

Begitu korban terkecoh dan menjalankan file eksekutabel utama (`f2413262...4243.exe`), program jahat ini tidak akan menampilkan aktivitas mencolok di layar. Sebaliknya, malware bekerja secara sembunyi-sembunyi (*stealth*) di latar belakang untuk menanamkan pengaruhnya pada sistem.

### Ringkasan Aktivitas Utama
1. **Persistence:** Mendaftarkan tiga *Scheduled Task* palsu yang menyamar sebagai proses sistem Windows (`WindowsUpdateService`, `MicrosoftUpdateTask`, dan `SystemHealthCheck`).
2. **Self-Replication:** Menduplikasi diri ke folder *Startup* (sebagai `Mjtasks.exe`) dan folder *Roaming* (sebagai `Scvtasks.exe`).
3. **Scripting:** Memanfaatkan eksekusi skrip PowerShell di folder `Temp` untuk menjalankan fungsi tambahan.
4. **Network Activity (Beaconing):** Mengirimkan lalu lintas HTTPS (Port 443) secara berulang ke alamat IP `2.23.246.9` guna melaporkan status perangkat target atau menunggu perintah selanjutnya dari penyerang.

---

## Infection Chain (Fase Eksekusi)

### Fase 1 – Initial Access (Ekstraksi Arsip)
Serangan dimulai ketika `WinRAR.exe` (PID `6336`) mengekstrak file *executable* dari arsip menuju direktori sementara:
`C:\Users\admin\AppData\Local\Temp\Rar$EXb6336.34186\`
File hasil ekstraksi (`f2413262c539ab550cdd01c88028bff17ee047d5482f0a28c03e3cc071bf4243.exe`) bertindak sebagai **payload utama**.
<img width="460" height="148" alt="Screenshot 2026-09-09 233047" src="https://github.com/user-attachments/assets/d3cc12be-ceb1-426e-a551-08ed3d0aed40" />


### Fase 2 – Persistence Setup (Scheduled Task)
Setelah dieksekusi (PID `912`), *payload* utama memanggil `cmd.exe` untuk membuat 3 *Scheduled Task* melalui `schtasks.exe` agar malware dapat berjalan otomatis pada sistem:
* `/tn "WindowsUpdateService"` *(dipanggil oleh `cmd.exe` PID `1828` ➔ `schtasks.exe` PID `6292`)*
* `/tn "MicrosoftUpdateTask"` *(dipanggil oleh `cmd.exe` PID `2176` ➔ `schtasks.exe` PID `6700`)*
* `/tn "SystemHealthCheck"` *(dipanggil oleh `cmd.exe` PID `6488` ➔ `schtasks.exe` PID `4284`)*
<img width="454" height="220" alt="Screenshot 2026-09-10 004752" src="https://github.com/user-attachments/assets/6feb543f-9970-4376-a2aa-4d1ba1f3e6cc" />
<img width="455" height="256" alt="Screenshot 2026-09-10 004811" src="https://github.com/user-attachments/assets/d50f5e44-4d11-4d14-b298-c95048d02344" />

### Fase 3 – Persistence Consolidation (Self-Copy)
Payload utama (PID `912`) menyalin dirinya ke dua lokasi tambahan di sistem:
* **Folder Startup:** `C:\Users\admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Mjtasks.exe`
* **Folder Roaming:** `C:\Users\admin\AppData\Roaming\Microsoft\Scvtasks.exe`
<img width="425" height="139" alt="Screenshot 2026-09-10 004519" src="https://github.com/user-attachments/assets/6ff137c6-d98c-491f-a445-e966d91d3396" />
<img width="438" height="155" alt="Screenshot 2026-09-10 004536" src="https://github.com/user-attachments/assets/fddc5897-29d0-4374-905d-f80c9658b9b5" />

### Fase 4 – Script Execution
Proses `powershell.exe` (PID `2412` dan PID `6984`) aktif membuat tiga artefak uji kebijakan eksekusi skrip (`PSScriptPolicyTest`) di direktori `Temp`:
* `_PSScriptPolicyTest_f02oa5az.sq2.ps1`
* `_PSScriptPolicyTest_qxpnnpta.ght.psm1`
* `_PSScriptPolicyTest_ijcjt540.f1w.ps1`
<img width="438" height="155" alt="Screenshot 2026-09-10 004536" src="https://github.com/user-attachments/assets/428191f5-f347-4129-83d5-554d505fdd89" />

### Fase 5 – Komunikasi Eksternal (Network Activity)
Pada aktivitas jaringan, `svchost.exe` (PID `1072`) melakukan lalu lintas komunikasi `POST` melalui jaringan HTTPS (Port 443) ke IP `2.23.246.9` (lokasi US). Seluruh permintaan tersebut menerima respons status `403: Forbidden`.
<img width="453" height="162" alt="Screenshot 2026-09-10 004929" src="https://github.com/user-attachments/assets/0307bf87-4a12-424c-98f9-32d2df2786f6" />

---

##  Execution & Process Tree

Analisis dinamis menunjukkan alur eksekusi malware yang diawali dari aksi pengguna hingga pembentukan mekanisme pertahanan dan teknik penyamaran (*Defense Evasion*):

1. **Initial Execution & Payload Launching:** Aktivitas diawali oleh pengguna yang membuka arsip melalui `WinRAR.exe` (PID: `6336`). Proses ini kemudian mengeksekusi file eksekutabel utama `f2413262...4243.exe` (PID: `912`) di folder Desktop sebagai payload utama.
2. **Persistence Mechanism via Command Line:** Sebagai induk proses (*parent process*), `f2413262...4243.exe` memanggil antarmuka baris perintah Windows untuk membuat tugas terjadwal (*Scheduled Tasks*):
   * `cmd.exe` (PID: `1828`): Dipanggil untuk mengeksekusi utilitas sistem `schtasks.exe` (PID: `6292`) guna meregistrasikan task `WindowsUpdateService`. Eksekusi perintah ini secara otomatis memicu proses pendukung konsol `conhost.exe` (PID: `5952`).
   * `cmd.exe` (PID: `2176`): Dipanggil untuk meregistrasikan task sekunder `MicrosoftUpdateTask`. Aktivitas konsol ini memicu dua sub-proses pendukung `conhost.exe` (PID: `7020`) dan `conhost.exe` (PID: `6700`).
3. **Defense Evasion & Process Masquerading:** Untuk menyembunyikan aktivitas berbahaya dari pemantauan sistem, malware memanfaatkan teknik *Living off the Land* (LotL) dengan mengeksekusi biner resmi Windows `dllhost.exe` (COM Surrogate).
<img width="452" height="222" alt="Screenshot 2026-09-10 015310" src="https://github.com/user-attachments/assets/d15bc75c-0100-45b1-afa9-a891dd325464" />
<img width="463" height="259" alt="Screenshot 2026-09-10 014926" src="https://github.com/user-attachments/assets/f1f47dd0-f39c-4073-8201-d73bfa3e9341" />

Berikut adalah bentuk visualisasi Process Tree secara singkat:

<img width="376" height="335" alt="Screenshot 2026-09-10 021357" src="https://github.com/user-attachments/assets/18f093d6-8249-41a2-ae16-df5a718c0db5" />

---

## MITRE ATT&CK Matrix Mapping


## MITRE ATT&CK Matrix & Event Breakdown

Berdasarkan hasil pemantauan dinamis pada sandbox ANY.RUN, sistem mencatat total **321 Events**, terklasifikasi ke dalam **14 Techniques**, dan tersebar di **5 Tactics**: *Execution*, *Persistence*, *Privilege Escalation*, *Defense Evasion*, dan *Discovery*.

### Legenda Warna (ANY.RUN Scheme)
* 🔴 **Danger** — Event dengan indikasi ancaman tinggi / berbahaya.
* 🟡 **Warning** — Event mencurigakan namun tidak selalu berbahaya.
* 🔵 **Other / Info** — Event informatif / aktivitas umum sistem.

> **Catatan Notasi:** Notasi `(x/y)` menunjukkan jumlah sub-technique yang terdeteksi `(x)` dari total sub-technique yang dikenal `(y)`.

---

### Execution (`TA0002`)

#### **T1053 – Scheduled Task/Job (1/6)**
* **Severity Summary:** 🔴 Danger 16 / 🟡 Warning 144 *(Total gabungan lintas 3 tactic: Execution, Persistence, Privilege Escalation)*
* **Deskripsi:** Penyalahgunaan fitur penjadwalan tugas bawaan OS (*Task Scheduler*) untuk menjalankan kode secara otomatis baik untuk eksekusi awal maupun menjaga persistensi.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Creates scheduled task with ONLOGON parameter` | 🟡 Warning | 30 | `f2413262...4243.exe` (2176) x5, `Mjtasks.exe` (2652) x5, `Scvtasks.exe` (7260) x5, + 15 instance `cmd.exe` |
| `Creates scheduled task with highest privileges` | 🟡 Warning | 30 | 15 pasangan `cmd.exe` → `schtasks.exe` (mis. PID 6780→7944, 6312→6972, 3304→7924) |
| `Uses Task Scheduler to autorun other applications` | 🔴 Danger | 88 | 88 instance `cmd.exe` berbeda (PID 6780, 3304, 5440, 440, 7148, 3336, 6080, 2160) |

*Sub-teknik lain seperti At, Cron, Launchd, Systemd Timers, dan Container Orchestration Job tidak terdeteksi (0 event / environment Windows).*

#### **T1059 – Command and Scripting Interpreter (2/13)**
* **Severity Summary:** 🟡 Warning 42
* **Deskripsi:** Interpreter baris perintah dan skrip bawaan sistem (*PowerShell*, *Windows Command Shell*) disalahgunakan untuk menjalankan perintah lanjutan.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Starts POWERSHELL.EXE for commands execution` | 🟡 Warning | 9 | 9 instance `cmd.exe` berbeda (PID 7772, 4584, 2372, 4748, 1668, 7300, 5764, 6352, 2448) |
| `Adds exclusion path to Windows Defender (POWERSHELL)` | 🟡 Warning | 9 | Sama seperti di atas (9 `cmd.exe` yang sama) |
| `Windows Command Shell` | 🟡 Warning | 24 | Total aktivitas eksekusi baris perintah `cmd.exe` |

---

### Persistence (`TA0003`)

#### **T1053 – Scheduled Task/Job**

#### **T1547 – Boot or Logon Autostart Execution (1/14)**
* **Severity Summary:** 🔴 Danger 10
* **Deskripsi:** Menjaga persistensi dengan menaruh entri di *Registry Run Key* atau folder *Startup* agar payload otomatis berjalan setiap kali sistem melakukan boot atau logon.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Changes the autorun value in the registry` | 🔴 Danger | 9 | `f2413262...4243.exe` (2176) x3, `Mjtasks.exe` (2652) x3, `Scvtasks.exe` (7260) x3 |
| `Create files in the Startup directory` | 🔴 Danger | 1 | `f2413262...4243.exe` (2176) x1 |

---

### Privilege Escalation (`TA0004`)

#### **T1053 – Scheduled Task/Job**

#### **T1547 – Boot or Logon Autostart Execution (1/14)**
* **Severity Summary:** 🔴 Danger 10
* **Deskripsi:** Dipetakan ke taktik *Privilege Escalation* karena entri autorun dan scheduled task dikonfigurasi untuk dieksekusi menggunakan konteks dan hak akses tertinggi yang tersedia.

---

### Defense Evasion (`TA0005`)

#### **T1497 – Virtualization/Sandbox Evasion (1/3)**
* **Severity Summary:** 🔴 Danger 8 / 🟡 Warning 1
* **Deskripsi:** Malware melakukan pemeriksaan lingkungan untuk mendeteksi apakah dirinya sedang dijalankan di dalam lingkungan analisis/sandbox.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Uses Task Scheduler to autorun other applications` | 🔴 Danger | 8 | 8 instance `cmd.exe` |
| `Reads the date of Windows installation` | 🟡 Warning | 1 | `f2413262...4243.exe` (2176) x1 |

#### **T1562 – Impair Defenses (1/12)**
* **Severity Summary:** 🔴 Danger 27 / 🟡 Warning 3
* **Deskripsi:** Upaya aktif melumpuhkan atau memodifikasi alat pertahanan sistem (*Windows Defender*).

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Changes Windows Defender settings` | 🔴 Danger | 9 | 9 instance `cmd.exe` berbeda (PID 7772, 4584, 2372, 4748, 1668, 7300, 5764, 6352, 2448) |
| `Adds path to the Windows Defender exclusion list` | 🔴 Danger | 18 | `f2413262...4243.exe` (2176) x3, `Mjtasks.exe` (2652) x3, `Scvtasks.exe` (7260) x3, + 9 `cmd.exe` x1 |
| `Found strings related to reading/modifying Windows Defender settings` | 🟡 Warning | 3 | `f2413262...4243.exe`, `Mjtasks.exe`, `Scvtasks.exe` (masing-masing 1x) |

#### **T1564 – Hide Artifacts (1/14)**
* **Severity Summary:** 🔴 Danger 9
* **Deskripsi:** Menjalankan proses tanpa jendela antarmuka (*windowless*) agar tidak diketahui oleh pengguna.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Run PowerShell with an invisible window` | 🔴 Danger | 9 | 9 instance `powershell.exe` (PID 4148, 5576, 3788, 5872, 2084, 5820, 1256, 6312, 4148) |


---

### Discovery (`TA0007`)

#### **T1012 – Query Registry**
* **Severity Summary:** 🟡 Warning 1 / 🔵 Other 43
* **Deskripsi:** Membaca *Windows Registry* untuk mengumpulkan informasi konfigurasi dan identitas sistem.

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Reads security settings of Internet Explorer` | 🔵 Other | 34 | `WinRAR.exe` (7420) x4, `f2413262...4243.exe` (2176) x10, `Mjtasks.exe` (2652) x10, `Scvtasks.exe` (7260) x10 |
| `Reads the machine GUID from the registry` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Reads the computer name` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Checks supported languages` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Reads the date of Windows installation` | 🟡 Warning | 1 | `f2413262...4243.exe` (2176) x1 |

#### **T1016 – System Network Configuration Discovery (0/2)**
* **Severity Summary:** 🟡 Warning 6
* **Deskripsi:** Memindai konfigurasi jaringan lokal sistem (*No suspicious behaviour details expanded*).

#### **T1082 – System Information Discovery**
* **Severity Summary:** 🟡 Warning 1 / 🔵 Other 9

| Event | Severity | Jumlah | Proses (PID) Representatif |
| :--- | :---: | :---: | :--- |
| `Reads the machine GUID from the registry` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Reads the computer name` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Checks supported languages` | 🔵 Other | 3 | Ketiga proses payload (masing-masing 1x) |
| `Reads the date of Windows installation` | 🟡 Warning | 1 | `f2413262...4243.exe` (2176) x1 |

#### **T1614 – System Location Discovery (0/1)**
* **Severity Summary:** 🔵 Other 1
* **Deskripsi:** Memeriksa wilayah geografis/lokasi sistem.

---

### Ringkasan Matriks MITRE ATT&CK

| Tactic | Tactic ID | Technique ID | Technique Name | Brief Event / Description |
| :--- | :---: | :--- | :--- | :--- |
| **Execution** | `TA0002` | **T1053** | Scheduled Task/Job | Membuat scheduled task untuk menjalankan payload secara otomatis |
| **Execution** | `TA0002` | **T1059** | Command and Scripting Interpreter | Eksekusi otomatis via PowerShell & Windows Command Shell |
| **Persistence** | `TA0003` | **T1053** | Scheduled Task/Job | Konfigurasi task `WindowsUpdateService` & `MicrosoftUpdateTask` |
| **Persistence** | `TA0003` | **T1547** | Boot or Logon Autostart Execution | Salinan payload di Registry Run Key / Startup Folder |
| **Privilege Escalation** | `TA0004` | **T1053** | Scheduled Task/Job | Task berjalan dengan hak akses dan konteks user |
| **Privilege Escalation** | `TA0004` | **T1547** | Boot or Logon Autostart Execution | Mempertahankan eksekusi otomatis berizin tinggi saat logon |
| **Defense Evasion** | `TA0005` | **T1497** | Virtualization/Sandbox Evasion | *Time-based check* untuk deteksi lingkungan sandbox |
| **Defense Evasion** | `TA0005` | **T1562** | Impair Defenses | Melumpuhkan/mengecualikan payload dari Windows Defender |
| **Defense Evasion** | `TA0005` | **T1564** | Hide Artifacts | Menjalankan proses PowerShell dengan jendela tersembunyi |
| **Discovery** | `TA0007` | **T1012** | Query Registry | Membaca registry sistem & konfigurasi keamanan |
| **Discovery** | `TA0007` | **T1082** | System Information Discovery | Mengumpulkan Machine GUID, Computer Name, & Info OS |
| **Discovery** | `TA0007` | **T1016** | System Network Configuration Discovery | Memindai konfigurasi adaptor jaringan |
| **Discovery** | `TA0007` | **T1614** | System Location Discovery | Memeriksa pengaturan lokasi/bahasa sistem |

<img width="893" height="376" alt="Screenshot 2026-09-11 030834" src="https://github.com/user-attachments/assets/463c79d0-6b72-4a6d-8625-1117e0a872cb" />
<img width="901" height="162" alt="Screenshot 2026-09-11 030848" src="https://github.com/user-attachments/assets/d1897cd8-9da4-4696-b3ae-a68fe327a840" />
---

## Indicators of Compromise (IoC) & Indicators of Attack (IoA)

---

### 1. Host-Based Indicators (IoA / IoC)

#### **Modified Registry Keys (IoA)**
Panel menunjukkan aktivitas modifikasi registry oleh proses sistem dan payload (seperti `WinRAR.exe` PID 6336 dan rantai proses `cmd.exe` / `schtasks.exe`). Terjadi operasi `Write` pada kunci registry pengguna (`HKEY_CURRENT_USER\SOFTWARE\...`) untuk pendaftaran artefak eksekusi. 

Dalam skenario serangan ini, malware memanfaatkan modifikasi kunci registry (seperti entri *Startup/Run* atau peretasan struktur `ms-settings`) untuk menjaga *persistence* agar tetap aktif saat sistem *reboot* serta mengeksekusi payload dengan hak akses tereskalasi (*UAC Bypass*).

#### **Process Anomaly (IoA)**
Terlihat pohon eksekusi yang tidak wajar di mana induk proses memanggil multiple `cmd.exe` (seperti PID 1828, 2176, 6488, 432) yang berlanjut pada pengeksekusian `schtasks.exe` dan `conhost.exe`. 

Anomali proses ini mencakup penyamaran eksekusi `dllhost.exe` dengan parameter `ProcessID GUID` khusus tanpa adanya pemanggilan objek COM resmi, yang digunakan malware untuk melakukan *process injection* atau penyusupan perintah tersembunyi ke dalam proses sistem Windows.
<img width="827" height="362" alt="Screenshot 2026-09-11 035151" src="https://github.com/user-attachments/assets/f42cdcdb-43b9-4188-8a1b-cbbd4ce1a322" />

---

### 2. Network-Based Indicators (IoC)

#### **IP Address (Defanged)**
* `2.23.246[.]9`

#### **Domain / URL Target (Defanged)**
* **Domain:** `go[.]microsoft[.]com` *(atau domain C2 khusus jika terhubung)*
* **URL:** `hxxps://go[.]microsoft[.]com/fwlink/?LinkId=2257403&clcid=0x409`
* **URL Tambahan (POST Request):** `hxxps://login[.]live[.]com/ppsecure/deviceaddcredential[.]srf`

#### **Port & Protocol**
* **Destination Port:** `443` (HTTPS) dan `80` (HTTP)
* **Protocol:** HTTP / HTTPS (Application Layer Protocol over TCP/TLS)

#### **Penjelasan Analisis Jaringan**
Pada **HTTP Request**, proses `svchost.exe` (PID 1072) tercatat melakukan pengiriman data keluar secara berulang menggunakan metode `POST` ke IP `2.23.246[.]9` pada port `443`. Meskipun URL terselubung menggunakan alamat pengalihan standar, aktivitas `POST` berulang dengan balasan status HTTP `403` dari PID tertentu mengindikasikan adanya lalu lintas *beaconing* / komunikasi fase *Command & Control* (C&C). 

**Connections** mengonfirmasi adanya koneksi aktif (*Connections*) berprotokol TLS/HTTPS (port 443) yang diinisiasi oleh `svchost.exe` (PID 1072) menuju infrastruktur tersebut.

<img width="827" height="362" alt="Screenshot 2026-09-11 035151" src="https://github.com/user-attachments/assets/450ec7f1-753a-444c-928a-b8e552b03cec" />

<img width="828" height="341" alt="Screenshot 2026-09-11 035342" src="https://github.com/user-attachments/assets/fa533480-bed0-473d-ae4d-b1071d714e77" />

---

## Recommendations & Mitigation

### 1. Deteksi & Pemantauan EDR/SIEM
* Buat aturan deteksi EDR/SIEM untuk memantau eksekusi `schtasks.exe` atau `powershell.exe` yang dipanggil langsung oleh file di folder pengguna (`AppData` / `Temp`).
* Pantau eksekusi `dllhost.exe` yang menggunakan parameter CLSID `{3E5FC7F9-9A51-4367-9063-A120244FBEC7}` atau yang dipanggil dari lokasi tidak wajar.

### 2. Pengerasan Sistem & Manajemen Hak Akses
* Batasi hak akses akun lokal (*Standard User*) untuk mencegah teknik bypass UAC otomatis.
* Terapkan kebijakan eksekusi PowerShell (*PowerShell Execution Policy*) yang ketat untuk membendung eksekusi skrip di folder `Temp`.

### 3. Respon Insiden & Isolasi Endpoint
* Isolasikan endpoint dari jaringan untuk memutus koneksi C2 ke IP `2.23.246[.]9`.
* Hapus Scheduled Tasks bernama `WindowsUpdateService`, `MicrosoftUpdateTask`, dan `SystemHealthCheck`.
* Bersihkan file eksekutabel `f2413262...4243.exe` dari direktori `Startup` dan `AppData\Roaming`.
