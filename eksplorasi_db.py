import mysql.connector
import pandas as pd

def jalankan_eksplorasi():
    try:
        # 1. Membuka jembatan koneksi dari aplikasi ke DBMS
        koneksi = mysql.connector.connect(
            host="localhost",
            user="root",        # Sesuaikan dengan user MySQL Anda
            password="",        # Kosongkan jika menggunakan XAMPP default
            database="db_akademik_ti"
        )
        print("[INFO] Koneksi ke MySQL Berhasil!\n")

        # 2. Mengirimkan perintah SQL melalui Python
        kueri = "SELECT * FROM kinerja_mahasiswa"
        
        # 3. Menampung hasil query ke dalam format DataFrame Pandas
        df = pd.read_sql(kueri, koneksi)

        # 4. Melakukan Eksplorasi Data Statistik (EDA)
        print("=== RINGKASAN STATISTIK KELAS BATCH 26 ===")
        
        # Menghitung jumlah mahasiswa per konsentrasi
        print("\n> Distribusi Konsentrasi Mahasiswa:")
        print(df['konsentrasi'].value_counts())
        
        # Mengeluarkan ringkasan metrik rata-rata, min, max dari nilai
        print("\n> Ringkasan Nilai Matakuliah & IPK:")
        print(df[['nilai_algoritma', 'nilai_basisdata', 'ipk_sementara']].describe())

    except mysql.connector.Error as err:
        print(f"[ERROR] Gagal terhubung ke database: {err}")
    
    finally:
        # Standar operasional prosedur: Selalu tutup koneksi setelah selesai
        if 'koneksi' in locals() and koneksi.is_connected():
            koneksi.close()
            print("\n[INFO] Koneksi database ditutup dengan aman.")

if __name__ == "__main__":
    jalankan_eksplorasi()