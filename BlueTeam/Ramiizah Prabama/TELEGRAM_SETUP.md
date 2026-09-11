# Menyiapkan Bot Telegram untuk Alert Wazuh

Sebelum integrasi Wazuh dijalankan, Anda perlu menyiapkan satu bot dan menentukan percakapan yang akan menerima notifikasi. Hasil dari proses ini adalah dua nilai:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
```

Token berfungsi sebagai kunci akses bot, sedangkan chat ID menunjukkan tujuan pengiriman pesan.

## Membuat bot

1. Buka Telegram dan cari akun resmi `@BotFather`.
2. Mulai percakapan, kemudian kirim perintah `/newbot`.
3. Tentukan nama yang mudah dikenali, misalnya `Wazuh Security Alerts`.
4. Buat username unik yang diakhiri dengan kata `bot`, misalnya `wazuh_security_lab_bot`.
5. Setelah proses selesai, BotFather akan memberikan token bot.

Bentuk token biasanya menyerupai contoh berikut:

```text
<TELEGRAM_BOT_TOKEN>
```

Simpan token tersebut di tempat aman. Siapa pun yang memilikinya dapat mencoba menggunakan API atas nama bot Anda.

## Mengaktifkan percakapan dengan bot

Bot tidak dapat mengawali percakapan pribadi dengan pengguna. Karena itu:

1. cari username bot yang baru dibuat;
2. buka halaman percakapannya;
3. tekan **Start**; dan
4. kirim satu pesan, misalnya `uji bot`.

Langkah ini membuat percakapan tersedia sebagai tujuan pengiriman alert.

## Mendapatkan chat ID

Untuk penggunaan pribadi, Anda dapat membuka `@userinfobot`, menekan **Start**, lalu mencatat ID numerik yang ditampilkan.

Contoh:

```text
123456789
```

Itulah nilai yang digunakan sebagai `CHAT_ID`. Bila notifikasi dikirim ke grup, ID grup dapat memiliki format berbeda dan biasanya diawali tanda minus; pastikan bot sudah ditambahkan ke grup tersebut.

## Menguji Telegram Bot API

Lakukan pengujian dari Wazuh Manager sebelum menghubungkannya dengan event Wazuh:

```bash
curl -s -X POST "https://api.telegram.org/botYOUR_TELEGRAM_BOT_TOKEN/sendMessage" \
  -d chat_id="YOUR_TELEGRAM_CHAT_ID" \
  -d text="Pengujian notifikasi dari Wazuh Manager"
```

Ganti kedua placeholder dengan token dan chat ID yang sebenarnya. Jika konfigurasi benar, Telegram akan mengembalikan respons dengan nilai `"ok": true` dan pesan pengujian muncul di chat tujuan.

Perhatikan bahwa perintah yang memuat token dapat tersimpan dalam riwayat shell. Hapus riwayat terkait setelah pengujian atau gunakan mekanisme input yang lebih aman pada lingkungan sensitif.

## Memasukkan nilai ke integrasi

Edit skrip yang telah ditempatkan pada server:

```bash
sudo nano /var/ossec/integrations/custom-telegram
```

Kemudian isi bagian berikut:

```python
TOKEN = "TOKEN_BOT_ANDA"
CHAT_ID = "ID_CHAT_ANDA"
```

Nilai asli hanya perlu tersedia pada Wazuh Manager. Biarkan versi yang dipublikasikan tetap menggunakan placeholder.

## Arti error yang umum

### `Bad Request: chat not found`

Telegram tidak menemukan percakapan tujuan. Periksa kembali chat ID, pastikan pengguna sudah menekan **Start**, atau pastikan bot telah menjadi anggota grup tujuan.

### `Unauthorized` atau `Not Found`

Token kemungkinan salah, sudah dicabut, atau URL API tidak tersusun dengan benar. Salin ulang token dari BotFather dan hindari spasi tambahan.

### Tidak ada respons dari server

Periksa koneksi internet, DNS, firewall, atau kebijakan jaringan Wazuh Manager. Server harus dapat membuat koneksi HTTPS menuju `api.telegram.org`.

### API berhasil tetapi alert Wazuh tidak masuk

Jika tes manual berhasil, sisi Telegram sudah siap. Lanjutkan pemeriksaan pada konfigurasi integrasi, level alert, permission skrip, dan log `integratord` sesuai [README.md](README.md).

## Menjaga kredensial

- Jangan menempelkan token di forum, commit Git, atau tangkapan layar.
- Jangan menyimpan token produksi pada komputer bersama.
- Buat ulang token melalui BotFather jika ada dugaan kebocoran.
- Batasi siapa yang dapat membaca skrip atau berkas tempat token disimpan.

Setelah pengujian berhasil, lanjutkan ke panduan pemasangan integrasi dalam [README.md](README.md).
