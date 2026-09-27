# 🎬 Auto Caption AI Gratis dengan Groq

Auto Caption AI adalah tool sederhana untuk membuat **caption/subtitle otomatis dari video menggunakan AI**.

Tool ini berjalan langsung di komputer Windows kamu dan menggunakan **Groq Whisper AI** untuk mengubah suara menjadi teks.

Kamu bisa:

- Upload video
- Generate caption otomatis dengan AI
- Edit teks caption
- Mengubah font
- Mengubah ukuran caption
- Mengubah warna
- Menambahkan outline dan shadow
- Memilih beberapa style caption
- Memilih animasi
- Preview caption
- Render caption langsung permanen ke video

> ⚠️ Tutorial ini dibuat khusus untuk **Windows** dan dibuat sesimpel mungkin untuk pemula.

---

# 1. Download Project

Klik tombol **Code** di repository GitHub ini.

Kemudian pilih:

**Download ZIP**

Setelah selesai:

1. Buka folder Downloads.
2. Cari file ZIP Auto-Caption.
3. Klik kanan.
4. Pilih **Extract All**.
5. Buka folder hasil extract.

Jangan jalankan program langsung dari dalam file ZIP.

---

# 2. Install Python

Kalau komputer kamu belum mempunyai Python, install Python terlebih dahulu dari website resmi Python.

Cari di Google:

**Python Download Windows**

Download Python untuk Windows lalu jalankan installer.

## PENTING

Saat installer Python muncul, centang:

**Add python.exe to PATH**

Kemudian pilih:

**Install Now**

Setelah selesai, tutup installer.

---

# 3. Buka CMD di Folder Auto Caption

Buka folder **Auto-Caption** yang tadi sudah di-extract.

Klik bagian address/path folder di atas File Explorer.

Ketik:

```text
cmd
```

Tekan **Enter**.

Command Prompt akan terbuka langsung di folder Auto-Caption.

Sekarang cek apakah Python berhasil terinstall:

```bash
py --version
```

Kalau muncul versi Python, berarti berhasil.

Contoh:

```text
Python 3.x.x
```

Kalau perintah `py` tidak bekerja, coba:

```bash
python --version
```

---

# 4. Install FFmpeg

Auto Caption membutuhkan **FFmpeg** untuk membaca audio dari video dan merender caption ke video.

Di CMD, jalankan:

```bash
winget install --id Gyan.FFmpeg -e
```

Tunggu sampai proses instalasi selesai.

Setelah selesai, **tutup CMD lalu buka CMD lagi**.

Kemudian cek:

```bash
ffmpeg -version
```

Kalau informasi FFmpeg muncul, berarti FFmpeg berhasil terinstall.

---

# 5. Install Library Python

Pastikan CMD masih berada di dalam folder Auto-Caption.

Jalankan:

```bash
py -m pip install -r requirements.txt
```

Tunggu sampai semuanya selesai terinstall.

Kalau komputer kamu menggunakan `python` dan bukan `py`, gunakan:

```bash
python -m pip install -r requirements.txt
```

---

# 6. Buat Groq API Key Gratis

Sekarang kita membutuhkan API Key agar AI bisa membuat caption.

Cari di Google:

**Groq Console**

Buka website resmi Groq.

Kemudian:

1. Login / buat akun Groq.
2. Masuk ke menu **API Keys**.
3. Klik **Create API Key**.
4. Beri nama API Key, misalnya:

```text
Auto Caption
```

5. Buat API Key.
6. Copy API Key yang diberikan.

API Key biasanya terlihat seperti secret key panjang.

## ⚠️ PENTING

Jangan pernah membagikan API Key kamu kepada orang lain.

Jangan upload API Key ke GitHub.

---

# 7. Masukkan Groq API Key

Di dalam CMD yang berada di folder Auto-Caption, jalankan:

```bash
copy .env.example .env
```

Kemudian buka file `.env`:

```bash
notepad .env
```

Isi file tersebut seperti ini:

```env
GROQ_API_KEY=MASUKKAN_API_KEY_KAMU_DI_SINI
```

Contoh:

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxx
```

Kemudian:

**Ctrl + S**

untuk Save.

Tutup Notepad.

---

# 8. Jalankan Auto Caption 🚀

Sekarang jalankan:

```bash
py app.py
```

Kalau `py` tidak bisa digunakan, gunakan:

```bash
python app.py
```

Kalau berhasil, browser akan terbuka otomatis dan Auto Caption siap digunakan.

Kalau browser tidak terbuka otomatis, lihat alamat local server yang muncul di CMD lalu buka melalui browser.

---

# 9. Cara Menggunakan Auto Caption

Setelah Auto Caption terbuka:

1. Klik **Upload**.
2. Pilih video.
3. Klik **Extract Audio & Text**.
4. Tunggu AI membuat transkripsi.
5. Periksa caption yang muncul.
6. Edit teks jika diperlukan.
7. Pilih font, warna, ukuran, outline, shadow, style, atau animasi.
8. Preview hasilnya.
9. Klik **Generate Permanen (Render)**.
10. Tunggu proses render selesai.

Setelah selesai, caption sudah menempel langsung ke video.

---

# 🤖 AI yang Digunakan

Auto Caption menggunakan:

**Groq + Whisper Large V3**

untuk melakukan Speech-to-Text.

Jadi suara dari video akan dikirim ke Groq untuk diubah menjadi teks dan timestamp caption.

---

# 💸 Apakah Gratis?

Project Auto Caption ini bisa digunakan secara gratis.

Groq menyediakan **Free Plan**, tetapi tetap memiliki batas penggunaan / rate limit.

Artinya ini bukan berarti API bisa digunakan unlimited tanpa batas.

Batas dari Groq juga dapat berubah sewaktu-waktu.

Untuk penggunaan normal dan testing, Free Plan dapat digunakan tanpa harus langsung menggunakan paket berbayar.

---

# ⚠️ Batas Ukuran Audio

Groq Free Plan memiliki batas ukuran file audio yang dikirim ke Speech-to-Text.

Kalau video terlalu panjang dan muncul error file terlalu besar, coba gunakan video yang lebih pendek terlebih dahulu.

Auto Caption secara otomatis mengekstrak audio dari video sebelum mengirimkannya ke AI.

---

# 🔧 Troubleshooting

## `'py' is not recognized`

Coba:

```bash
python app.py
```

Kalau `python` juga tidak ditemukan, install ulang Python dan pastikan:

**Add python.exe to PATH**

sudah dicentang.

---

## `'ffmpeg' is not recognized`

Pastikan FFmpeg sudah diinstall:

```bash
winget install --id Gyan.FFmpeg -e
```

Setelah selesai:

**tutup CMD dan buka kembali CMD.**

Lalu cek:

```bash
ffmpeg -version
```

---

## `ModuleNotFoundError`

Jalankan lagi:

```bash
py -m pip install -r requirements.txt
```

---

## Error Groq / API Key

Periksa file:

```text
.env
```

Pastikan formatnya:

```env
GROQ_API_KEY=API_KEY_KAMU
```

Jangan menggunakan API Key milik orang lain.

---

## `TemplateNotFound: index.html`

Pastikan struktur foldernya seperti ini:

```text
Auto-Caption/
│
├── app.py
├── main.py
├── config.py
│
└── templates/
    └── index.html
```

File `index.html` **harus berada di dalam folder `templates`**.

---

# 🔐 Keamanan API Key

Jangan pernah upload file:

```text
.env
```

ke repository GitHub.

Repository ini menggunakan `.gitignore` agar file tersebut tidak ikut terupload.

Yang boleh ada di GitHub adalah:

```text
.env.example
```

karena file tersebut tidak berisi API Key asli.

---

# ❤️ Selesai

Kalau Auto Caption sudah terbuka di browser dan kamu sudah bisa upload video:

**SELAMAT 🎉**

Auto Caption AI sudah berhasil terinstall di komputer kamu.

Sekarang tinggal:

**Upload → Generate Caption → Edit → Render.**

Enjoy! 🚀
