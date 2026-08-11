import customtkinter as ctk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageDraw
import rembg
import io
import os

# Setup Tema
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MacGlassApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ===== Konfigurasi Window =====
        self.title("macOS Glass UI - Background Remover")
        self.geometry("1280x800")
        self.minsize(1000, 700)
        
        # Hilangkan bingkai jendela bawaan OS (Borderless)
        self.overrideredirect(True)
        
        # Variabel
        self.original_image = None
        self.processed_image = None
        self.final_image = None
        self.bg_image = None
        self.current_bg_color = (88, 86, 214, 255) # Ungu macOS
        
        # Membuat latar belakang gradient blur
        self.create_blurred_background()
        
        # Bind mouse untuk menggerakkan window (karena borderless)
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_move)
        
        # Bind untuk mengembalikan borderless saat di-restore dari taskbar
        self.bind("<Map>", self.on_map)
        
        # Build UI
        self.create_title_bar()
        self.create_main_layout()

    # ==========================================
    # CUSTOM WINDOW & GLASS EFFECT
    # ==========================================
    def create_blurred_background(self):
        bg_img = Image.new("RGB", (1400, 900))
        draw = ImageDraw.Draw(bg_img)
        
        # Warna gradient khas macOS (Pink, Ungu, Biru)
        colors = [(255, 105, 180), (138, 43, 226), (72, 61, 139), (30, 144, 255)]
        for i in range(len(colors)):
            x_start = int((i / len(colors)) * 1400)
            x_end = int(((i + 1) / len(colors)) * 1400)
            draw.rectangle([x_start, 0, x_end, 900], fill=colors[i])
            
        # Mengaplikasikan blur ekstrem untuk efek Frosted Glass
        self.bg_blurred = bg_img.filter(ImageFilter.GaussianBlur(150))
        
        # Gunakan CTkImage agar tidak warning HighDPI
        self.bg_photo = ctk.CTkImage(light_image=self.bg_blurred, dark_image=self.bg_blurred, size=(1400, 900))
        
        # Set sebagai background window
        self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="", fg_color="transparent")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_title_bar(self):
        # Titlebar transparent/glass style
        self.title_bar = ctk.CTkFrame(self, height=40, fg_color="gray10", corner_radius=0, bg_color="gray10")
        self.title_bar.pack(fill="x", side="top")
        
        # Judul di tengah
        self.title_label = ctk.CTkLabel(self.title_bar, text="Photo Studio", 
                                        font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
                                        text_color="white")
        self.title_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Tombol Traffic Light (Mac Style)
        btn_close = ctk.CTkButton(self.title_bar, text="", width=14, height=14, corner_radius=7,
                                  fg_color="#FF5F57", hover_color="#E0443E", command=self.quit)
        btn_close.place(x=15, rely=0.5, anchor="w")
        
        btn_min = ctk.CTkButton(self.title_bar, text="", width=14, height=14, corner_radius=7,
                                 fg_color="#FEBC2E", hover_color="#DEA123", command=self.minimize)
        btn_min.place(x=35, rely=0.5, anchor="w")
        
        btn_max = ctk.CTkButton(self.title_bar, text="", width=14, height=14, corner_radius=7,
                                fg_color="#28C840", hover_color="#1AAB29", command=self.toggle_maximize)
        btn_max.place(x=55, rely=0.5, anchor="w")

    def create_main_layout(self):
        # Frame Utama dengan efek gelap semi-transparan (Glass Panel)
        self.main_container = ctk.CTkFrame(self, corner_radius=20, fg_color="gray10")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # ===== SIDEBAR (Kiri) =====
        self.sidebar = ctk.CTkFrame(self.main_container, width=260, corner_radius=15, fg_color="transparent")
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Watermark di bagian paling bawah sidebar
        ctk.CTkLabel(self.sidebar, text="Made By Monnalisa-ID\nVersion 2.0 (Glass UI)", 
                     font=ctk.CTkFont(family="Helvetica", size=12), 
                     text_color="gray40", justify="center").pack(side="bottom", pady=20, fill="x")

        # Judul Aplikasi (Atas)
        ctk.CTkLabel(self.sidebar, text="🎨 Magic Studio", 
                     font=ctk.CTkFont(family="Helvetica", size=22, weight="bold")).pack(pady=(20, 30), padx=20)

        # Tombol-tombol Menu
        ctk.CTkButton(self.sidebar, text="📁  Buka Foto", command=self.load_image, height=42, 
                      fg_color="gray20", hover_color="gray30", corner_radius=10).pack(pady=8, padx=20, fill="x")
        
        ctk.CTkButton(self.sidebar, text="✂️  Hapus Background", command=self.remove_background, height=42, 
                      fg_color="#E74C3C", hover_color="#C0392B", corner_radius=10).pack(pady=8, padx=20, fill="x")

        ctk.CTkLabel(self.sidebar, text="— GANTI LATAR —", font=ctk.CTkFont(size=11, weight="bold"), 
                     text_color="gray50").pack(pady=(20, 5), padx=20, anchor="w")

        ctk.CTkButton(self.sidebar, text="🎨  Warna Solid", command=self.choose_bg_color, height=38, 
                      fg_color="#2ECC71", hover_color="#27AE60", corner_radius=10).pack(pady=6, padx=20, fill="x")
        
        ctk.CTkButton(self.sidebar, text="🖼️  Gambar Latar", command=self.choose_bg_image, height=38, 
                      fg_color="#9B59B6", hover_color="#8E44AD", corner_radius=10).pack(pady=6, padx=20, fill="x")

        ctk.CTkButton(self.sidebar, text="💾  Simpan Hasil", command=self.save_image, height=42, 
                      fg_color="#F39C12", hover_color="#D35400", corner_radius=10).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(self.sidebar, text="🔄  Reset", command=self.reset, height=38, 
                      fg_color="transparent", border_width=1, border_color="gray40", 
                      text_color="gray70", hover_color="gray20", corner_radius=10).pack(pady=5, padx=20, fill="x")

        # ===== AREA KERJA (Kanan) =====
        self.workspace = ctk.CTkFrame(self.main_container, corner_radius=15, fg_color="transparent")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_columnconfigure(1, weight=1)
        self.workspace.grid_rowconfigure(1, weight=1)

        self.status_var = ctk.StringVar(value="✅ Siap digunakan")
        self.status_label = ctk.CTkLabel(self.workspace, textvariable=self.status_var, height=35, 
                                        fg_color="gray20", corner_radius=8, anchor="w", padx=15,
                                        font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"))
        self.status_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        self.panel_orig = ctk.CTkFrame(self.workspace, corner_radius=12, fg_color="gray15")
        self.panel_orig.grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        ctk.CTkLabel(self.panel_orig, text="Foto Asli", font=ctk.CTkFont(size=14, weight="bold", family="Helvetica")).pack(pady=10)
        self.lbl_original = ctk.CTkLabel(self.panel_orig, text="Tidak ada gambar", text_color="gray50")
        self.lbl_original.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.panel_res = ctk.CTkFrame(self.workspace, corner_radius=12, fg_color="gray15")
        self.panel_res.grid(row=1, column=1, sticky="nsew", padx=(5, 0))
        ctk.CTkLabel(self.panel_res, text="Hasil Akhir", font=ctk.CTkFont(size=14, weight="bold", family="Helvetica")).pack(pady=10)
        self.lbl_result = ctk.CTkLabel(self.panel_res, text="Tidak ada gambar", text_color="gray50")
        self.lbl_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ==========================================
    # FUNGSI WINDOW MAC OS
    # ==========================================
    def start_move(self, event):
        if event.widget == self.title_bar or event.widget == self.title_label:
            self.x = event.x
            self.y = event.y

    def on_move(self, event):
        if hasattr(self, 'x') and hasattr(self, 'y'):
            x = self.winfo_x() + (event.x - self.x)
            y = self.winfo_y() + (event.y - self.y)
            self.geometry(f"+{x}+{y}")

    def minimize(self):
        # Trik agar borderless window bisa di-minimize ke taskbar
        self.overrideredirect(False)
        self.iconify()

    def on_map(self, event):
        # Mengembalikan borderless window setelah di-restore dari taskbar
        if self.state() == 'normal':
            self.overrideredirect(True)

    def toggle_maximize(self):
        if self.state() == 'normal':
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        else:
            self.geometry("1280x800")

    # ==========================================
    # LOGIKA GAMBAR
    # ==========================================
    def load_image(self):
        file_path = filedialog.askopenfilename(title="Pilih Foto", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            try:
                self.original_image = Image.open(file_path).convert("RGB")
                self.display_image(self.original_image, self.lbl_original)
                self.processed_image = None
                self.final_image = None
                self.lbl_result.configure(image=None, text="Tidak ada gambar")
                self.status_var.set(f"🖼️ Foto dimuat: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat gambar:\n{e}")

    def remove_background(self):
        if self.original_image is None:
            messagebox.showwarning("Peringatan", "Silakan buka foto terlebih dahulu!")
            return

        self.status_var.set("⏳ Memproses... Mohon tunggu...")
        self.update_idletasks()

        try:
            img_byte_arr = io.BytesIO()
            self.original_image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()

            result_bytes = rembg.remove(img_bytes)
            self.processed_image = Image.open(io.BytesIO(result_bytes)).convert("RGBA")

            self.apply_background()
            self.status_var.set("✅ Background berhasil dihapus!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus background:\n{e}")

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Pilih Warna Latar")
        if color[0] is not None:
            self.current_bg_color = tuple(int(c) for c in color[0]) + (255,)
            self.bg_image = None
            if self.processed_image is not None:
                self.apply_background()
            self.status_var.set(f"🎨 Latar diubah ke warna: {color[1]}")

    def choose_bg_image(self):
        file_path = filedialog.askopenfilename(title="Pilih Gambar Latar", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            try:
                self.bg_image = Image.open(file_path).convert("RGB")
                if self.processed_image is not None:
                    self.apply_background()
                self.status_var.set(f"🖼️ Latar diubah ke gambar: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memuat gambar latar:\n{e}")

    def apply_background(self):
        if self.processed_image is None: return

        if self.bg_image is not None:
            bg = self.bg_image.resize(self.processed_image.size, Image.LANCZOS).convert("RGBA")
        else:
            bg = Image.new("RGBA", self.processed_image.size, self.current_bg_color)

        self.final_image = Image.alpha_composite(bg, self.processed_image)
        self.display_image(self.final_image, self.lbl_result)

    def save_image(self):
        if self.final_image is None:
            messagebox.showwarning("Peringatan", "Tidak ada hasil untuk disimpan!")
            return

        file_path = filedialog.asksaveasfilename(title="Simpan Hasil", defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if file_path:
            try:
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    self.final_image.convert("RGB").save(file_path, quality=95)
                else:
                    self.final_image.save(file_path)
                self.status_var.set(f"💾 Hasil disimpan: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Gagal menyimpan:\n{e}")

    def display_image(self, image, label):
        self.update_idletasks()
        max_w = label.winfo_width() - 20
        max_h = label.winfo_height() - 20
        if max_w < 100 or max_h < 100: max_w, max_h = 450, 450

        img_copy = image.copy()
        img_copy.thumbnail((max_w, max_h), Image.LANCZOS)
        
        # FIX WARNING: Gunakan CTkImage alih-alih ImageTk.PhotoImage
        ctk_img = ctk.CTkImage(light_image=img_copy, dark_image=img_copy, size=img_copy.size)
        
        label.configure(image=ctk_img, text="")
        label.image = ctk_img  # Simpan referensi

    def reset(self):
        self.original_image = None
        self.processed_image = None
        self.final_image = None
        self.bg_image = None
        self.lbl_original.configure(image=None, text="Tidak ada gambar")
        self.lbl_result.configure(image=None, text="Tidak ada gambar")
        self.status_var.set("🔄 Direset - siap digunakan")


if __name__ == "__main__":
    app = MacGlassApp()
    app.mainloop()