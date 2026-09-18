import csv
import os

FILE_NAME= 'data_buku.csv'

# Proses Implementasi Menambahkan Data
def tambah_buku(id_buku, judul, penulis):
    # Mode append ('a') untuk menambahkan baris di akhir file
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_buku, judul, penulis])
    print(f"File System: Buku {judul} berhasil di tambahkan.")

# Proses Implementasi Membaca data
def lihat_buku():
    print("\n--- Daftar Buku (File CSV) ---")
    if not os.path.exists(FILE_NAME):
        print("File Belum ada.")
        return
    with open(FILE_NAME, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(f"ID:{row[0]}, Judul: {row[1]}, Penulis: {row[2]}")

# MENGUBAH DATA
def ubah_buku(id_cari, judul_baru):
    buku_list =[]
    # Baca semua file isi ke memori
    with open(FILE_NAME,mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id_cari:
                row[1] = judul_baru # update data
            buku_list.append(row)

# Proses tulis ulang seluruh file dengan data yang baru
    with open(FILE_NAME,mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(buku_list)
    print(f"File System: Data buku ID {id_cari} berhasil diubah!")

# Proses Menjalankan program
if __name__ == "__main__":
    tambah_buku('B01','Logika Algoritma','Andi')
    tambah_buku('B02','Sistem Operasi','Budi')
    lihat_buku()
    ubah_buku('B01','Algoritma Lanjut')
    lihat_buku()