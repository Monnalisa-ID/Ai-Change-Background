# 🎨 Magic Studio — AI Background Changer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.x-1f6feb?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-PIL-brightgreen?style=for-the-badge)
![rembg](https://img.shields.io/badge/rembg-AI%20Powered-ff6b6b?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Aplikasi desktop berdesain macOS Glass UI untuk menghapus & mengganti latar belakang foto secara otomatis menggunakan AI.**

</div>

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🤖 **AI Background Removal** | Hapus latar belakang foto secara otomatis menggunakan model AI `rembg` |
| 🎨 **Ganti dengan Warna Solid** | Pilih warna apapun sebagai latar belakang baru via color picker |
| 🖼️ **Ganti dengan Gambar Latar** | Gunakan foto/gambar lain sebagai background baru |
| 💾 **Ekspor Hasil** | Simpan hasil akhir dalam format PNG atau JPEG |
| 🪟 **macOS Glass UI** | Tampilan borderless dengan efek Frosted Glass khas macOS |
| 📷 **Preview Side-by-side** | Tampilkan foto asli dan hasil akhir secara berdampingan |

---

## 🖥️ Tampilan Aplikasi

Aplikasi menggunakan desain **macOS Glass UI** dengan:
- Gradient blur background berwarna Pink → Ungu → Biru
- Custom title bar dengan tombol traffic light (merah, kuning, hijau)
- Panel kontrol sidebar yang bersih dan intuitif
- Mode gelap (Dark Mode) secara default

---

## 🚀 Cara Instalasi

### Prasyarat
- Python **3.8** atau lebih baru
- `pip` (sudah termasuk dalam instalasi Python)

### 1. Clone / Download Repository

```bash
git clone https://github.com/Monnalisa-ID/Ai-ChangeBackground.git
cd "Ai Change Background"
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

> ⚠️ **Catatan:** `rembg` akan mengunduh model AI (~170 MB) secara otomatis saat pertama kali dijalankan. Pastikan koneksi internet tersedia.

---

## ▶️ Cara Menjalankan

```bash
python changebg.py
```

---

## 📖 Cara Penggunaan

1. **Buka Foto** — Klik tombol `📁 Buka Foto` dan pilih gambar (PNG, JPG, JPEG, BMP)
2. **Hapus Background** — Klik `✂️ Hapus Background` dan tunggu proses AI selesai
3. **Ganti Latar** — Pilih salah satu opsi:
   - `🎨 Warna Solid` → pilih warna dari color picker
   - `🖼️ Gambar Latar` → pilih gambar sebagai background baru
4. **Simpan Hasil** — Klik `💾 Simpan Hasil` untuk mengekspor gambar akhir
5. **Reset** — Klik `🔄 Reset` untuk memulai dari awal

---

## 📦 Dependensi

| Library | Versi Minimum | Fungsi |
|---------|--------------|--------|
| `customtkinter` | ≥ 5.2.0 | Framework UI modern berbasis Tkinter |
| `Pillow` | ≥ 10.0.0 | Pemrosesan dan manipulasi gambar |
| `rembg` | ≥ 2.0.50 | AI model untuk penghapusan background |

---

## 🗂️ Struktur Proyek

```
Ai Change Background/
│
├── changebg.py         # File utama aplikasi
├── requirements.txt    # Daftar dependensi Python
├── README.md           # Dokumentasi proyek
└── LICENSE             # Lisensi MIT
```

---

## ⚙️ Teknologi yang Digunakan

- **[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)** — Modern UI framework untuk Python
- **[rembg](https://github.com/danielgatis/rembg)** — Library AI untuk menghapus background foto (berbasis U²-Net)
- **[Pillow (PIL)](https://python-pillow.org/)** — Library pemrosesan gambar Python
- **Tkinter** — Library GUI bawaan Python (digunakan untuk dialog & color picker)

---

## 🔧 Troubleshooting

**❌ Error saat install rembg**
```bash
# Coba install dengan versi spesifik
pip install rembg==2.0.50
```

**❌ Model AI tidak terunduh**
> Pastikan koneksi internet aktif saat pertama kali menjalankan `Hapus Background`. Model disimpan di folder cache sistem.

**❌ Tampilan aplikasi tidak muncul / crash**
> Pastikan semua dependensi terinstall dengan benar:
```bash
pip install -r requirements.txt --upgrade
```

**❌ Window tidak bisa dipindahkan**
> Klik dan tahan pada area **title bar** (area hitam di atas) untuk memindahkan window.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat file [LICENSE](LICENSE) untuk detail lengkapnya.

---

<div align="center">

Made with ❤️ by **Monnalisa-ID** &nbsp;|&nbsp; Version 2.0 (Glass UI)

</div>
