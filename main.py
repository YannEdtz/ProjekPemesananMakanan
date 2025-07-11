import csv
from linked_list import LinkedList
from stack import Stack

DATA_FILE = 'data_pesanan.csv'

def load_data():
    pesanan_list = LinkedList()
    try:
        with open(DATA_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pesanan_list.tambah(row)
    except FileNotFoundError:
        open(DATA_FILE, 'w').close()
    return pesanan_list

def simpan_data(pesanan_list):
    with open(DATA_FILE, mode='w', newline='') as file:
        fieldnames = ['ID', 'Nama Pemesan', 'Menu', 'Jumlah']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for p in pesanan_list.tampil():
            writer.writerow(p)

def main():
    pesanan = load_data()
    undo_stack = Stack()

    while True:
        print("\n=== Aplikasi Pemesanan Makanan ===")
        print("1. Tambah Pesanan")
        print("2. Tampilkan Semua Pesanan")
        print("3. Cari Pesanan (ID)")
        print("4. Hapus Pesanan")
        print("5. Undo Hapus")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            id_pesanan = input("ID Pesanan: ")
            nama = input("Nama Pemesan: ")
            menu = input("Menu yang Dipesan: ")
            jumlah = input("Jumlah Porsi: ")
            pesanan.tambah({'ID': id_pesanan, 'Nama Pemesan': nama, 'Menu': menu, 'Jumlah': jumlah})
            simpan_data(pesanan)
            print("Pesanan berhasil ditambahkan.")

        elif pilihan == '2':
            semua = pesanan.tampil()
            if semua:
                for p in semua:
                    print(p)
            else:
                print("Belum ada data pesanan.")

        elif pilihan == '3':
            id_pesanan = input("Masukkan ID Pesanan: ")
            hasil = pesanan.cari(id_pesanan)
            if hasil:
                print("Pesanan ditemukan:", hasil)
            else:
                print("Pesanan tidak ditemukan.")

        elif pilihan == '4':
            id_pesanan = input("ID Pesanan yang akan dihapus: ")
            dihapus = pesanan.hapus(id_pesanan)
            if dihapus:
                undo_stack.push(dihapus)
                simpan_data(pesanan)
                print("Pesanan berhasil dihapus.")
            else:
                print("Pesanan tidak ditemukan.")

        elif pilihan == '5':
            if not undo_stack.is_empty():
                kembali = undo_stack.pop()
                pesanan.tambah(kembali)
                simpan_data(pesanan)
                print("Undo berhasil. Pesanan dikembalikan.")
            else:
                print("Tidak ada pesanan untuk di-undo.")

        elif pilihan == '0':
            print("Terima kasih telah menggunakan aplikasi pemesanan makanan.")
            break

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()