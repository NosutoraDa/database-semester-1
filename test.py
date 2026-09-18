import mysql.connector

# Koneksi ke MySQL
db = mysql.connector.connect(host="localhost", 
user="root", 
password="", 
database="db_perpustakaan2026")
cursor = db.cursor()

# 1. CREATE (Menambahkan Data)
def tambah_buku_db(id_buku, judul, penulis):
    sql = "INSERT INTO buku (id_buku, judul, penulis) VALUES (%s, %s, %s)"
    val = (id_buku, judul, penulis)
    cursor.execute(sql, val)
    db.commit() # Simpan permanen
    print(f"DBMS: Buku {judul} berhasil disimpan ke database.")

# 2. READ (Membaca Data)
def lihat_buku_db():
    print("\n--- Daftar Buku (MySQL) ---")
    cursor.execute("SELECT * FROM buku")
    for row in cursor.fetchall():
        print(f"ID: {row[0]}, Judul: {row[1]}, Penulis: {row[2]}")

# 3. UPDATE (Mengubah Data) - SANGAT RINGKAS
def ubah_buku_db(id_cari, judul_baru):
    sql = "UPDATE buku SET judul = %s WHERE id_buku = %s"
    val = (judul_baru, id_cari)
    cursor.execute(sql, val)
    db.commit()
    print(f"DBMS: Data buku ID {id_cari} berhasil diubah.")

# ===== SIMULASI EKSEKUSI =====
if __name__ == "__main__":
    tambah_buku_db('B01', 'Logika Algoritma', 'Andi')
    tambah_buku_db('B02', 'Sistem Operasi', 'Budi')
    lihat_buku_db()
    ubah_buku_db('B01', 'Algoritma Lanjut') # Simulasi Update
    lihat_buku_db()
