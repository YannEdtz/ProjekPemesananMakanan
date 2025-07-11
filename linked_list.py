class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def tambah(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def tampil(self):
        hasil = []
        current = self.head
        while current:
            hasil.append(current.data)
            current = current.next
        return hasil

    def cari(self, id_pesanan):
        current = self.head
        while current:
            if current.data['ID'] == id_pesanan:
                return current.data
            current = current.next
        return None

    def hapus(self, id_pesanan):
        current = self.head
        prev = None
        while current:
            if current.data['ID'] == id_pesanan:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return current.data
            prev = current
            current = current.next
        return None