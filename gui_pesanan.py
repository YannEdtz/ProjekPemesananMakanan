import tkinter as tk
from tkinter import ttk, messagebox
import csv

DATA_FILE = 'data_pesanan.csv'
undo_stack = []

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🛒 Aplikasi Pemesanan Makanan")
        self.root.geometry("600x500")
        self.root.configure(bg="#f8f9fa")
        
        self.setup_widgets()
        self.load_data()

    def setup_widgets(self):
        # Judul
        title = tk.Label(self.root, text="🛒 Aplikasi Pemesanan Makanan", font=("Helvetica", 16, "bold"), bg="#f8f9fa")
        title.pack(pady=10)

        # Form Frame
        form_frame = tk.Frame(self.root, bg="#f8f9fa")
        form_frame.pack(pady=5)

        labels = ["ID", "Nama Pemesan", "Menu", "Jumlah"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label, bg="#f8f9fa", anchor="w").grid(row=i, column=0, sticky="w")
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=3)
            self.entries[label] = entry

        # Tombol
        btn_frame = tk.Frame(self.root, bg="#f8f9fa")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Tambah", width=10, bg="#28a745", fg="white", command=self.tambah).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Hapus", width=10, bg="#dc3545", fg="white", command=self.hapus).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Undo", width=10, bg="#ffc107", command=self.undo).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Cari", width=10, bg="#007bff", fg="white", command=self.cari).grid(row=0, column=3, padx=5)

        # Tabel Data
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nama", "Menu", "Jumlah"), show="headings", height=10)
        for col in ("ID", "Nama", "Menu", "Jumlah"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def tambah(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Input Tidak Lengkap", "Semua field harus diisi.")
            return

        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        self.clear_form()
        self.load_data()

    def hapus(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Pilih data yang ingin dihapus.")
            return

        values = self.tree.item(selected[0])['values']
        undo_stack.append(values)

        data_baru = []
        with open(DATA_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] != values[0]:
                    data_baru.append(row)

        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['ID', 'Nama Pemesan', 'Menu', 'Jumlah'])
            writer.writeheader()
            writer.writerows(data_baru)

        self.load_data()

    def undo(self):
        if not undo_stack:
            messagebox.showinfo("Undo", "Tidak ada data untuk di-undo.")
            return

        last = undo_stack.pop()
        data = {
            "ID": last[0],
            "Nama Pemesan": last[1],
            "Menu": last[2],
            "Jumlah": last[3]
        }

        with open(DATA_FILE, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)

        self.load_data()

    def cari(self):
        id_cari = self.entries["ID"].get()
        if not id_cari:
            messagebox.showinfo("Cari", "Masukkan ID untuk mencari.")
            return

        found = False
        for row in self.tree.get_children():
            if self.tree.item(row)['values'][0] == id_cari:
                self.tree.selection_set(row)
                self.tree.see(row)
                found = True
                break

        if not found:
            messagebox.showinfo("Hasil", f"ID {id_cari} tidak ditemukan.")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            with open(DATA_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert('', 'end', values=(row['ID'], row['Nama Pemesan'], row['Menu'], row['Jumlah']))
        except FileNotFoundError:
            pass

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()