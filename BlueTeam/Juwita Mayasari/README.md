# Blue Team Final Project: Defensive Security & Threat Analysis

## Malicious File Analysis with ANY.RUN

Tittle: Dynamic Analysis of Vidar Information Stealer
Date: 30 August 2026
Analyst: Juwita Mayasari

### 1. File Information & Threat Verdict
Analisis dilakukan terhadap sampel malware Vidar yang diperoleh dari MalwareBazaar. Sampel kemudian dianalisis secara dinamis menggunakan platform ANY.RUN dalam lingkungan yang terisolasi.
- File Name: 2e6d42ec2312a5df0ef24d3bec6b5dfb29627c8a8073be2edd6facea2ac96ab8.zip
- Threat Verdict: Malicious (Score: 100/100)
- Tags: arch-exec, telegram, and evasion
- Target OS: Windows 10 (64-bit)

### 2. Executive Summary
Sebuah arsip ZIP berbahaya dieksekusi secara manual oleh pengguna, yang kemudian menyebabkan dijalankannya sebuah file executable dengan sertifikat yang tidak tepercaya. File executable tersebut melakukan pemeriksaan terhadap lingkungan sistem dan sandbox untuk menghindari deteksi, serta melakukan komunikasi dengan infrastruktur Telegram.

### 3. Execution & Process Tree
Dari hasil ANY.RUN, executable Vidar dijalankan setelah ZIP diekstrak oleh WinRAR.

- Process Name:
2e6d42ec2312a5df0ef24d3bec6b5dfb29627c8a8073be2edd6facea2ac96ab8.exe
- Path: C:\Users\admin\AppData\Local\Temp\Rar$EXb5924.38718\2e6d42ec2312a5df0ef24d3bec6b5dfb29627c8a8073be2edd6facea2ac96ab8.exe
- Command Line: "C:\Users\admin\AppData\Local\Temp\Rar$EXb5924.38718\2e6d42ec2312a5df0ef24d3bec6b5dfb29627c8a8073be2edd6facea2ac96ab8.exe"

### 4. MITRE ATT&CK Framework Mapping
Berdasarkan analisis perilaku, sampel ini memicu beberapa taktik dan teknik MITRE ATT&CK:
| Tactic | Technique ID | Technique Name | Description / Event |
| Defense Evasion | T1497 | Virtualization/Sandbox Evasion	| Malware memeriksa apakah dirinya sedang dijalankan di lingkungan virtual atau sandbox untuk menghindari proses analisis. |
| Defense Evasion	| T1497.001	| System Checks	| Malware melakukan pemeriksaan terhadap lingkungan sistem dengan membaca versi BIOS dan registry key tertentu yang berkaitan dengan lingkungan virtual. |
| Discovery |	T1082 |	System Information Discovery |	Malware mengumpulkan informasi mengenai sistem, termasuk versi BIOS dan nama komputer. |
| Discovery |	T1012 |	Query Registry	| Malware melakukan query terhadap Windows Registry, termasuk membaca registry key tertentu dari VM serta informasi terkait versi BIOS dan nama komputer. |

### 5. Indicators of Compromise (IoC) & Indicators of Attack (IoA)
- Host Based Indicators (IoA/IoC):
    - Virtualization/Sandbox Check: Malware memeriksa apakah dirinya dijalankan dalam lingkungan virtual atau sandbox untuk mendeteksi lingkungan analisis.
    - BIOS Information Query: Malware membaca versi BIOS untuk memperoleh informasi mengenai sistem yang sedang digunakan.
    - Registry Query: Malware membaca registry key tertentu yang berkaitan dengan lingkungan virtual atau sistem.
    - Computer Name Discovery: Malware membaca nama komputer untuk memperoleh informasi identitas host.
    - Instant Messaging Service Activity: Malware terdeteksi melakukan aktivitas yang berkaitan dengan layanan pesan instan, dalam hal ini Telegram.

- Network-Based Indicators (IoC):
    - Domain: Telegram[.]me
    - Destination IP: 149[.]154[.]167[.]99 
    - Protocol: TLS
    - Port: 443

### 6. Recommendations & Mitigation
- Terapkan pemantauan EDR/SIEM untuk mendeteksi aktivitas seperti query Registry dan pengumpulan informasi sistem.
- Pantau dan blokir koneksi keluar menuju IP atau domain yang teridentifikasi sebagai indikator sampel.
- Batasi eksekusi file .exe dari direktori sementara seperti %TEMP%, terutama file yang berasal dari arsip ZIP yang tidak terpercaya.
- Terapkan prinsip least privilege dan hindari penggunaan akun administrator untuk aktivitas sehari-hari.
- Isolasi endpoint yang terindikasi terinfeksi dari jaringan dan lakukan investigasi lebih lanjut.
- Perbarui sistem operasi, antivirus/EDR, dan database threat intelligence secara berkala.

Full Analysis: [https://app.any.run/tasks/1764efcd-8ce6-4895-b618-28e7b796bf5e]