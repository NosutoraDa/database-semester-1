from logging import root
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
import hashlib
import subprocess
import sys

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "dbPerpusNew2026"

#FUNGSI MEMBUAT TABEL BUKU
def inisialisasi_tabel_buku():
    try:
        conn_db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        kursor_db = conn_db.cursor()

        sql_buat_tabel = """
        CREATE TABLE IF NOT EXISTS tblBuku (
            idBuku VARCHAR(20) PRIMARY KEY,
            judulBuku VARCHAR(100) NOT NULL,
            penerbit VARCHAR(100) NOT NULL,
            pengarang VARCHAR(100) NOT NULL,
            jumlahBuku INT NOT NULL
        )
        """
        kursor_db.execute(sql_buat_tabel)
        conn_db.close()

    except Error as e:
        messagebox.showerror("Error", f"Gagal menginisialisasi tabel buku: {e}")

#FUNGSI KONEKSI DATABASE
def koneksi():
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except Error:
        return "Databasenya tidak ditemukan. Silakan buat database terlebih dahulu."

def tampil_data():
    """Membaca dan menampilkan data dari database ke Treeview."""
    # Bersihkan isi Treeview sebelumnya
    for baris in tree.get_children():
        tree.delete(baris)
        
    db = koneksi()
    if db is None: return
    
    try:
        kursor = db.cursor()
        kursor.execute("SELECT * FROM tblBuku ORDER BY idBuku ASC")
        hasil = kursor.fetchall()
        
        # Masukkan data ke Treeview
        for baris_data in hasil:
            tree.insert("", tk.END, values=baris_data)
            
    except Error as e:
        messagebox.showerror("Error", f"Gagal menampilkan data: {e}")
    finally:
        db.close()

def simpan_data():
    """Menyimpan data buku baru ke database (Create)."""
    id_buku = var_id.get().strip()
    judul = var_judul.get().strip()
    penerbit = var_penerbit.get().strip()
    pengarang = var_pengarang.get().strip()
    jumlah = var_jumlah.get().strip()
    
    if not id_buku or not judul or not penerbit or not pengarang or not jumlah:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return
        
    db = koneksi()
    if db is None: return
    
    try:
        kursor = db.cursor()
        sql = "INSERT INTO tblBuku (idBuku, judulBuku, penerbit, pengarang, jumlahBuku) VALUES (%s, %s, %s, %s, %s)"
        kursor.execute(sql, (id_buku, judul, penerbit, pengarang, jumlah))
        db.commit()
        
        messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
        bersihkan_form()
        tampil_data()
    except mysql.connector.IntegrityError:
        messagebox.showerror("Gagal", f"ID Buku '{id_buku}' sudah ada di database!")
    except Error as e:
        messagebox.showerror("Error", f"Gagal menyimpan data: {e}")
    finally:
        db.close()

def ubah_data():
    """Mengubah data buku yang sudah ada (Update)."""
    id_buku = var_id.get().strip()
    judul = var_judul.get().strip()
    penerbit = var_penerbit.get().strip()
    pengarang = var_pengarang.get().strip()
    jumlah = var_jumlah.get().strip()
    
    if not id_buku:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah terlebih dahulu!")
        return
        
    db = koneksi()
    if db is None: return
    
    try:
        kursor = db.cursor()
        sql = """UPDATE tblBuku 
                 SET judulBuku=%s, penerbit=%s, pengarang=%s, jumlahBuku=%s 
                 WHERE idBuku=%s"""
        kursor.execute(sql, (judul, penerbit, pengarang, jumlah, id_buku))
        db.commit()
        
        messagebox.showinfo("Sukses", "Data buku berhasil diubah!")
        bersihkan_form()
        tampil_data()
    except Error as e:
        messagebox.showerror("Error", f"Gagal mengubah data: {e}")
    finally:
        db.close()

def hapus_data():
    """Menghapus data buku (Delete)."""
    id_buku = var_id.get().strip()
    
    if not id_buku:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus terlebih dahulu!")
        return
        
    konfirmasi = messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus buku dengan ID '{id_buku}'?")
    if not konfirmasi: return
        
    db = koneksi()
    if db is None: return
    
    try:
        kursor = db.cursor()
        sql = "DELETE FROM tblBuku WHERE idBuku=%s"
        kursor.execute(sql, (id_buku,))
        db.commit()
        
        messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
        bersihkan_form()
        tampil_data()
    except Error as e:
        messagebox.showerror("Error", f"Gagal menghapus data: {e}")
    finally:
        db.close()

def bersihkan_form():
    """Mengosongkan semua kolom input."""
    var_id.set("")
    var_judul.set("")
    var_penerbit.set("")
    var_pengarang.set("")
    var_jumlah.set("")
    input_id.focus()

def isi_form_dari_tabel(event):
    """Mengisi kolom input saat salah satu baris di Treeview diklik."""
    baris_terpilih = tree.focus()
    if not baris_terpilih: return
    
    data = tree.item(baris_terpilih, 'values')
    if data:
        var_id.set(data[0])
        var_judul.set(data[1])
        var_penerbit.set(data[2])
        var_pengarang.set(data[3])
        var_jumlah.set(data[4])

inisialisasi_tabel_buku()  # Pastikan tabel buku ada sebelum menjalankan GUI

#GUI

root = tk.Tk()
root.title("Kelola Data Buku")
root.geometry("800x600")
root.config(bg="#f4f6f9")

# Posisikan ke tengah layar
x = int((root.winfo_screenwidth() / 2) - (800 / 2))
y = int((root.winfo_screenheight() / 2) - (600 / 2))
root.geometry(f"+{x}+{y}")

# Judul
tk.Label(root, text="FORM DATA BUKU", font=("Helvetica", 16, "bold"), bg="#f4f6f9").pack(pady=15)

# Variabel Input
var_id = tk.StringVar()
var_judul = tk.StringVar()
var_penerbit = tk.StringVar()
var_pengarang = tk.StringVar()
var_jumlah = tk.StringVar()

# Frame Form Input
frame_input = tk.Frame(root, bg="#ffffff", padx=20, pady=20, relief="solid", bd=1)
frame_input.pack(fill="x", padx=20, pady=10)

# Baris 1: ID & Judul
tk.Label(frame_input, text="ID Buku", font=("Arial", 10, "bold"), bg="#ffffff").grid(row=0, column=0, sticky="w", pady=5, padx=5)
input_id = tk.Entry(frame_input, textvariable=var_id, width=15, font=("Arial", 11))
input_id.grid(row=0, column=1, sticky="w", pady=5, padx=5)

tk.Label(frame_input, text="Judul Buku", font=("Arial", 10, "bold"), bg="#ffffff").grid(row=0, column=2, sticky="w", pady=5, padx=20)
tk.Entry(frame_input, textvariable=var_judul, width=35, font=("Arial", 11)).grid(row=0, column=3, sticky="w", pady=5, padx=5)

# Baris 2: Penerbit & Pengarang
tk.Label(frame_input, text="Penerbit", font=("Arial", 10, "bold"), bg="#ffffff").grid(row=1, column=0, sticky="w", pady=5, padx=5)
tk.Entry(frame_input, textvariable=var_penerbit, width=35, font=("Arial", 11)).grid(row=1, column=1, columnspan=3, sticky="w", pady=5, padx=5)

tk.Label(frame_input, text="Pengarang", font=("Arial", 10, "bold"), bg="#ffffff").grid(row=2, column=0, sticky="w", pady=5, padx=5)
tk.Entry(frame_input, textvariable=var_pengarang, width=35, font=("Arial", 11)).grid(row=2, column=1, columnspan=3, sticky="w", pady=5, padx=5)

# Baris 3: Jumlah Buku
tk.Label(frame_input, text="Jumlah Buku", font=("Arial", 10, "bold"), bg="#ffffff").grid(row=3, column=0, sticky="w", pady=5, padx=5)
tk.Entry(frame_input, textvariable=var_jumlah, width=10, font=("Arial", 11)).grid(row=3, column=1, sticky="w", pady=5, padx=5)

# Frame Tombol Aksi
frame_tombol = tk.Frame(root, bg="#f4f6f9")
frame_tombol.pack(fill="x", padx=20, pady=5)

tk.Button(frame_tombol, text="Simpan", command=simpan_data, bg="#198754", fg="white", width=12, font=("Arial", 10, "bold")).pack(side="left", padx=5)
tk.Button(frame_tombol, text="Ubah", command=ubah_data, bg="#0d6efd", fg="white", width=12, font=("Arial", 10, "bold")).pack(side="left", padx=5)
tk.Button(frame_tombol, text="Hapus", command=hapus_data, bg="#dc3545", fg="white", width=12, font=("Arial", 10, "bold")).pack(side="left", padx=5)
tk.Button(frame_tombol, text="Bersihkan", command=bersihkan_form, bg="#6c757d", fg="white", width=12, font=("Arial", 10, "bold")).pack(side="left", padx=5)

# Frame Tabel Data (Treeview)
frame_tabel = tk.Frame(root, padx=20, pady=10, bg="#f4f6f9")
frame_tabel.pack(fill="both", expand=True)

kolom = ("ID Buku", "Judul Buku", "Penerbit", "Pengarang", "Jumlah")
tree = ttk.Treeview(frame_tabel, columns=kolom, show="headings", height=10)

# Konfigurasi Header dan Lebar Kolom
lebar_kolom = [100, 250, 150, 150, 80]
for col, lebar in zip(kolom, lebar_kolom):
    tree.heading(col, text=col)
    tree.column(col, width=lebar, anchor="w")

# Tambahkan Scrollbar
scrollbar = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)

# Event Binding: Klik pada baris di Treeview untuk mengisi form
tree.bind("<ButtonRelease-1>", isi_form_dari_tabel)

# Jalankan fungsi tampil data saat form pertama kali terbuka
tampil_data()

root.mainloop()
