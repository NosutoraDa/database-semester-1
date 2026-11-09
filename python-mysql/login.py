from logging import root
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import hashlib
import subprocess
import sys

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "dbPerpusNew2026"

#FUNGSI MEMBUAT TABEL DAN DATABASE KALO BELUM ADA
def inisialisasi_database_dan_tabel():
    # membuat database jika belum ada
    try:
        conn_server = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
        kursor_server = conn_server.cursor()
        kursor_server.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn_server.close()

        conn_db = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        kursor_db = conn_db.cursor()

        sql_buat_tabel = """
        CREATE TABLE IF NOT EXISTS tbl_pengguna (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
        """
        kursor_db.execute(sql_buat_tabel)
        conn_db.close()

    except Error as e:
        messagebox.showerror("Error", f"Gagal menginisialisasi database dan tabel: {e}")

#FUNGSI KONEKSI DATABASE
def koneksi():
    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except Error:
        return None

#FUNGSI ENKRIPSI PASSWORD
def enkripsi_password(password_asli):
    return hashlib.sha256(password_asli.encode()).hexdigest()   

#FUNGSI REGISTER
def proses_register():
    username = input_user.get().strip()
    password = input_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Peringatan", "Username dan password tidak boleh kosong.")
        return

    password_enkripsi = enkripsi_password(password)
    db = koneksi()
    if not db:
        return

    try:
        kursor = db.cursor()
        sql = "INSERT INTO tbl_pengguna (username, password) VALUES (%s, %s)"
        kursor.execute(sql, (username, password_enkripsi))
        db.commit()
        messagebox.showinfo("Sukses", "Registrasi berhasil! Silakan login.")
        input_pass.delete(0, tk.END)
    except mysql.connector.IntegrityError:
        messagebox.showerror("Gagal", f"Username {username} sudah digunakan. Silakan pilih username lain.")
    except Error as e:
        messagebox.showerror("Error", f"Terjadi Kesalahan: {e}")
    finally:
        db.close()

 #FUNGSI LOGIN
def proses_login():
    username = input_user.get().strip()
    password = input_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Peringatan", "Username dan password tidak boleh kosong.")
        return

    password_enkripsi = enkripsi_password(password)
    db = koneksi()

    if db is None:
        messagebox.showerror("Error", "Gagal terhubung ke database.")
        return

    try:
        kursor = db.cursor()
        sql = "SELECT username FROM tbl_pengguna WHERE username = %s AND password = %s"
        kursor.execute(sql, (username, password_enkripsi))
        akun_ditemukan = kursor.fetchone()

        if akun_ditemukan:
            messagebox.showinfo("Sukses", f"Selamat datang, {username}!")

            #Jendela login
            root.destroy()

            #Buka Menu Utama
            file_tujuan = "buku.py"
            try:
                subprocess.Popen([sys.executable, file_tujuan])
            except Exception as e:
                messagebox.showerror("Error", f"Gagal membuka {file_tujuan}: {e}")

        else:
            messagebox.showerror("Gagal", "Username atau password salah.")

    except Error as e:
        messagebox.showerror("Error", f"Terjadi Kesalahan: {e}")
    finally:
        db.close()

inisialisasi_database_dan_tabel()

root = tk.Tk()
root.title("Login")
root.geometry("350x400")
root.eval('tk::PlaceWindow . center')
root.config(bg="#f0f0f0")
root.resizable(False, True)

x = (root.winfo_screenwidth() - 350) // 2
y = (root.winfo_screenheight() - 400) // 2
root.geometry(f"+{x}+{y}")

tk.Label(root, text="FORM LOGIN", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=(30, 20))

frame_form = tk.Frame(root, bg="#f0f0f0", padx=15, pady=20)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Username", font=("Arial", 12), bg="#f0f0f0", fg="#555").pack(anchor="w")
input_user = tk.Entry(frame_form, font=("Arial", 12), width=30)
input_user.pack(pady=5)

tk.Label(frame_form, text="Password", font=("Arial", 12), bg="#f0f0f0", fg="#555").pack(anchor="w")
input_pass = tk.Entry(frame_form, font=("Arial", 12), width=30, show="*")
input_pass.pack(pady=5)

tk.Button(frame_form, text="Login", font=("Arial", 12), width=30, command=proses_login, bg="#2196F3", fg="white", activebackground="#2196F3").pack(pady=10)
tk.Button(frame_form, text="Register", font=("Arial", 12), width=30, command=proses_register, bg="#45a049", fg="white", activebackground="#45a049").pack(pady=10)

root.mainloop()