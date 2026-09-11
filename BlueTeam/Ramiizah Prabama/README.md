# Notifikasi Keamanan Wazuh melalui Telegram

Repositori ini berisi integrasi ringan untuk meneruskan alert dari Wazuh Manager ke percakapan Telegram. Saat sebuah event memenuhi level yang ditentukan, Wazuh menjalankan skrip Python, memberikan lokasi file alert berformat JSON, lalu skrip menyusun ringkasan dan mengirimkannya melalui Telegram Bot API.

## Alur kerja

```text
Endpoint dipantau
       |
       v
Wazuh Agent mengumpulkan event
       |
       v
Wazuh Manager mengevaluasi rule
       |
       v
custom-telegram membaca alert JSON
       |
       v
Telegram Bot API mengirim notifikasi
```

Informasi yang dicantumkan dalam pesan meliputi:

- nama agent;
- level alert;
- ID rule;
- deskripsi kejadian; dan
- lokasi sumber log.

## Isi repositori

```text
.
|-- custom-telegram.py
|-- README.md
|-- TELEGRAM_SETUP.md
|-- wazuh_telegram_alert_plan.png
```

## Persiapan

Sebelum memasang integrasi, pastikan hal berikut tersedia:

- akses administratif ke Wazuh Manager;
- Python 3;
- modul Python `requests`;
- token bot Telegram; dan
- ID chat tujuan.

Jika modul `requests` belum tersedia pada Wazuh Manager, pasang sesuai metode pengelolaan paket Python pada sistem operasi yang digunakan.

## Pemasangan pada Wazuh Manager

### 1. Tempatkan skrip integrasi

Salin skrip ke direktori integrasi Wazuh dan hilangkan ekstensi `.py` pada nama tujuan:

```bash
sudo cp custom-telegram.py /var/ossec/integrations/custom-telegram
```

Nama tersebut harus sama dengan nilai `<name>` yang nanti digunakan di `ossec.conf`.

### 2. Isi kredensial Telegram

Buka skrip yang sudah disalin:

```bash
sudo nano /var/ossec/integrations/custom-telegram
```

Ganti nilai contoh berikut dengan data bot milik Anda:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
```

Jangan menyimpan token asli dalam repository publik. Untuk lingkungan produksi, pertimbangkan menyimpan kredensial di environment variable atau berkas rahasia yang hanya dapat dibaca oleh proses terkait.

### 3. Atur kepemilikan dan mode file

Wazuh perlu dapat mengeksekusi skrip tersebut:

```bash
sudo chown root:wazuh /var/ossec/integrations/custom-telegram
sudo chmod 750 /var/ossec/integrations/custom-telegram
```

Dengan konfigurasi ini, pemilik memperoleh akses penuh, anggota grup `wazuh` dapat membaca dan menjalankan, sedangkan pengguna lain tidak memperoleh akses.

### 4. Daftarkan integrasi

Edit konfigurasi Wazuh Manager:

```bash
sudo nano /var/ossec/etc/ossec.conf
```

Tambahkan blok berikut di dalam elemen `<ossec_config>`:

```xml
<integration>
  <name>custom-telegram</name>
  <level>10</level>
  <alert_format>json</alert_format>
</integration>
```

Nilai `level` menentukan batas minimum alert yang diteruskan. Ubah angka tersebut apabila Anda hanya ingin menerima alert dengan tingkat tertentu. Format JSON wajib dipertahankan karena skrip membaca file alert menggunakan parser JSON.

### 5. Terapkan konfigurasi

Restart Wazuh Manager:

```bash
sudo /var/ossec/bin/wazuh-control restart
```

Setelah layanan kembali aktif, buat event pengujian yang memenuhi level integrasi dan periksa apakah notifikasi masuk ke Telegram.

## Pemeriksaan ketika pesan tidak masuk

Pantau log integrasi Wazuh:

```bash
sudo tail -f /var/ossec/logs/ossec.log | grep -a -E "integratord|custom-telegram"
```

Pastikan nama, pemilik, dan permission skrip sesuai:

```bash
ls -l /var/ossec/integrations/custom-telegram
```

Hasilnya kurang lebih harus seperti berikut:

```text
-rwxr-x--- 1 root wazuh ... /var/ossec/integrations/custom-telegram
```

Gunakan daftar pemeriksaan ini jika masalah masih terjadi:

1. Pastikan bot sudah pernah dibuka dan tombol **Start** sudah ditekan.
2. Uji token serta chat ID langsung melalui Telegram API.
3. Pastikan server dapat mengakses `api.telegram.org`.
4. Periksa apakah event mencapai level minimum pada konfigurasi integrasi.
5. Pastikan `<alert_format>json</alert_format>` tidak terhapus.
6. Pastikan Wazuh Manager sudah direstart setelah konfigurasi diubah.

Jika log menampilkan `FileNotFoundError`, periksa argumen yang diterima skrip. Pada konfigurasi ini, Wazuh memberikan lokasi file alert melalui argumen pertama:

```python
alert_file = sys.argv[1]
```

## Catatan keamanan

- Jangan mengunggah token bot ke GitHub, tangkapan layar, atau issue tracker.
- Jika token terlanjur tersebar, cabut token melalui BotFather dan buat token baru.
- Gunakan permission file yang ketat pada server.
- Pilih level alert secara wajar agar chat tidak dipenuhi event berprioritas rendah.

Panduan pembuatan bot dan pengambilan chat ID tersedia di [TELEGRAM_SETUP.md](TELEGRAM_SETUP.md).
