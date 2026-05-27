# Auto Input Data Rinex

Proyek ini adalah sebuah utilitas Python untuk mengunduh file RINEX dari layanan SRGI (Badan Informasi Geospasial Indonesia) menggunakan akun terdaftar. Proyek ini terletak di folder `getData` dan menggunakan sesi HTTP untuk login dan mengambil file ZIP dari server.

## Struktur Proyek

- `getData/`
  - `main.py` - entry point utama skrip unduhan.
  - `config.py` - konfigurasi URL, header, dan direktori penyimpanan hasil unduhan.
  - `auth/login.py` - fungsi login untuk otentikasi ke layanan menggunakan email dan password.
  - `downloader/rinex.py` - logika untuk membangun payload permintaan, memanggil endpoint unduhan, dan menyimpan file ZIP.
  - `grpc_utils/` - utilitas untuk membangun payload gRPC yang diperlukan oleh API.
  - `utils/` - utilitas tambahan untuk decoding respons gRPC-Web.
- `GPS_TEC.exe`, `GPS_TEC.ini`, `runGPS.bat`, `runGPS-auto.bat`, `run.vbs` - file tambahan/eksekusi yang mungkin terkait dengan alur penggunaan aplikasi.
- `ZIPLOG/`, `IGS_Stations.txt` - data pendukung.

## Persyaratan

- Python 3.x
- Paket Python:
  - `requests`
  - `python-dotenv`
  - `beautifulsoup4`

> Catatan: Tidak ada berkas `requirements.txt` di repo ini, jadi instalasi paket harus dilakukan secara manual.

## Persiapan

1. Salin file `.env.example` menjadi `.env` di dalam folder `getData`.
2. Isi dengan akun SRGI Anda:

```env
EMAIL="email@contoh.com"
PASSWORD="password_anda"
```

3. Periksa dan sesuaikan variabel `directory` di `getData/config.py`.
   - Saat ini nilai default adalah `E:/rinex/`.
   - Ubah ke folder lokal Anda jika diperlukan.
   - Pastikan folder tujuan sudah ada atau buat terlebih dahulu.

## Cara Menjalankan

1. Buka terminal di folder utama proyek `GPS_Gopi_v3.5`.
2. Jalankan skrip Python dari dalam folder `getData`:

```powershell
cd getData
python main.py
```

3. Program akan melakukan:
   - login ke `https://srgi.big.go.id`
   - mengambil daftar stasiun preset
   - mengunduh file ZIP RINEX untuk setiap stasiun
   - menyimpan file ZIP ke folder yang ditentukan di konfigurasi

## Penjelasan Singkat Alur

1. `main.py` memuat konfigurasi dan variabel email/password dari `.env`.
2. Fungsi `login()` melakukan GET ke halaman login untuk mengambil token CSRF dan cookie XSRF.
3. Setelah login berhasil, `main.py` memanggil `download_rinex()` untuk setiap stasiun.
4. `download_rinex()` membangun payload gRPC menggunakan utilitas `grpc_utils.payload`, memanggil API unduhan, lalu menyimpan file ZIP yang diterima.

## Daftar Stasiun

Skrip default akan men-download data untuk stasiun berikut:

- `bako`
- `cang`
- `cbik`
- `cdnp`
- `samp`
- `cbda`
- `cmak`

## Tips

- Jika Anda ingin menambah atau mengubah stasiun, edit daftar `stations` di `getData/main.py`.
- Jika terjadi error login, pastikan email/password benar dan akun Anda terdaftar di layanan.
- Jika unduhan ZIP gagal, periksa kembali URL dan header di `getData/config.py`.

## Lisensi

Tidak ada informasi lisensi dalam repo ini. Gunakan sesuai kebutuhan dan pastikan mematuhi kebijakan layanan SRGI.
