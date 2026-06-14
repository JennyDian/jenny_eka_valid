import streamlit as st
from datetime import date
import random

# =====================================
# NODE
# =====================================

class Node:
    def __init__(
        self,
        nama,
        alamat,
        email,
        no_telp,
        tanggal_lahir,
        kategori,
        harga,
        jumlah,
        total,
        pembayaran,
        kode_tiket,
        status_cetak="Belum Dicetak"
    ):
        self.nama = nama
        self.alamat = alamat
        self.email = email
        self.no_telp = no_telp
        self.tanggal_lahir = tanggal_lahir
        self.kategori = kategori
        self.harga = harga
        self.jumlah = jumlah
        self.total = total
        self.pembayaran = pembayaran
        self.kode_tiket = kode_tiket
        self.status_cetak = status_cetak
        self.next = None


# =====================================
# LINKED LIST
# =====================================

class LinkedList:
    def __init__(self):
        self.head = None

    # Tambah Data
    def tambah(
        self,
        nama,
        alamat,
        email,
        no_telp,
        tanggal_lahir,
        kategori,
        harga,
        jumlah,
        total,
        pembayaran,
        kode_tiket
    ):
        node_baru = Node(
            nama,
            alamat,
            email,
            no_telp,
            tanggal_lahir,
            kategori,
            harga,
            jumlah,
            total,
            pembayaran,
            kode_tiket
        )
        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru

    # Tampilkan Data
    def tampilkan(self):
        data = []
        current = self.head
        while current:
            data.append({
                "Kode Tiket": current.kode_tiket,
                "Nama": current.nama,
                "Alamat": current.alamat,
                "Email": current.email,
                "No Telepon": current.no_telp,
                "Tanggal Lahir": current.tanggal_lahir,
                "Kategori": current.kategori,
                "Harga Tiket": f"Rp {current.harga:,}",
                "Jumlah Tiket": current.jumlah,
                "Total Harga": f"Rp {current.total:,}",
                "Metode Pembayaran": current.pembayaran,
                "Status Cetak": current.status_cetak
            })
            current = current.next
        return data

    # Cari Data Berdasarkan Nomor Telepon
    def cari_by_telp(self, no_telp):
        current = self.head
        while current:
            if current.no_telp.strip() == no_telp.strip():
                return current
            current = current.next
        return None

    # Hapus Data Berdasarkan Nama
    def hapus(self, nama):
        current = self.head
        prev = None
        while current:
            if current.nama.lower() == nama.lower():
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False

    # Cetak Tiket Berdasarkan Nama
    def cetak_tiket(self, nama):
        current = self.head
        while current:
            if current.nama.lower() == nama.lower():
                current.status_cetak = "Sudah Dicetak"
                return current
            current = current.next
        return None


# =====================================
# SESSION STATE
# =====================================

if "tiket" not in st.session_state:
    st.session_state.tiket = LinkedList()


# =====================================
# HARGA TIKET
# =====================================

harga_tiket = {
    "VIP": 8000000,
    "CAT 1": 4500000,
    "CAT 2": 3000000,
    "CAT 3": 2000000
}


# =====================================
# HEADER
# =====================================

st.title("🎤 Tiket Konser Justin Bieber")
st.write(
    "Sistem Pemesanan Tiket Konser Justin Bieber Menggunakan Linked List"
)


# =====================================
# DAFTAR HARGA
# =====================================

st.subheader("🎫 Daftar Harga Tiket")

st.info("""
VIP : Rp 8.000.000  
CAT 1 : Rp 4.500.000  
CAT 2 : Rp 3.000.000  
CAT 3 : Rp 2.000.000
""")


# =====================================
# INITIALIZE STATE UNTUK HARGA TAMPILAN
# =====================================
if "harga_tampil" not in st.session_state:
    st.session_state.harga_tampil = 0
if "total_tampil" not in st.session_state:
    st.session_state.total_tampil = 0


# =====================================
# 1. FORM PEMESANAN
# =====================================

st.subheader("📝 Form Pemesanan Tiket")

with st.form("form_pemesanan", clear_on_submit=True):
    nama = st.text_input("Nama Pemesan")
    alamat = st.text_area("Alamat")
    email = st.text_input("Email")
    no_telp = st.text_input("No. Telepon")

    tanggal_lahir = st.date_input(
        "Tanggal Lahir",
        min_value=date(1900, 1, 1),
        max_value=date(2008, 12, 31),
        value=None,
    ) 

    kategori = st.selectbox(
        "Pilih Kategori Tiket",
        ["Pilih Kategori Tiket", "VIP", "CAT 1", "CAT 2", "CAT 3"]
    )

    jumlah = st.number_input(
        "Jumlah Tiket",
        min_value=0,
        max_value=4,
        step=1,
        value=0 
    )

    metode_pembayaran = st.selectbox(
        "Metode Pembayaran",
        [
            "Pilih Metode Pembayaran",
            "Debit",
            "QRIS",
            "GoPay",
            "DANA"
        ]
    )

    if kategori == "Pilih Kategori Tiket" or jumlah == 0 or not nama:
        harga_asli = 0
        total_asli = 0
        st.session_state.harga_tampil = 0
        st.session_state.total_tampil = 0
    else:
        harga_asli = harga_tiket[kategori]
        total_asli = harga_asli * jumlah
        st.session_state.harga_tampil = harga_asli
        st.session_state.total_tampil = total_asli

    st.write(f"### Harga Tiket : Rp {st.session_state.harga_tampil:,}")
    st.write(f"### Total Harga : Rp {st.session_state.total_tampil:,}")

    submit = st.form_submit_button("Tambah Pemesan")


# --- LOGIKA TOMBOL SUBMIT ---
if submit:
    if not nama:
        st.warning("Masukkan nama!")
    elif not alamat:
        st.warning("Masukkan alamat!")
    elif not email:
        st.warning("Masukkan email!")
    elif not no_telp:
        st.warning("Masukkan nomor telepon!")
    elif kategori == "Pilih Kategori Tiket":
        st.warning("Silakan pilih kategori tiket yang valid!")
    elif jumlah == 0:
        st.warning("Jumlah tiket minimal harus 1!")
    elif metode_pembayaran == "Pilih Metode Pembayaran":
        st.warning("Silakan pilih metode pembayaran!")
    else:
        # Generate otomatis Kode Tiket Unik
        acak_angka = random.randint(10000, 99999)
        kode_tiket_baru = f"JB-2026-{acak_angka}"

        st.session_state.tiket.tambah(
            nama,
            alamat,
            email,
            no_telp,
            tanggal_lahir,
            kategori,
            harga_asli,
            jumlah,
            total_asli,
            metode_pembayaran,
            kode_tiket_baru
        )

        st.session_state.harga_tampil = 0
        st.session_state.total_tampil = 0

        st.success("✅ Pesanan berhasil ditambahkan")
        st.success(f"💳 Pembayaran berhasil! Kode Tiket Anda: {kode_tiket_baru}")
        st.balloons()
        
        st.rerun()


# =====================================
# 2. DAFTAR PEMESAN (SATU-SATUNYA)
# =====================================
st.write("---")
st.subheader("📋 Daftar Pemesan")
data_pemesan = st.session_state.tiket.tampilkan()

if data_pemesan:
    st.table(data_pemesan)
else:
    st.info("Belum ada data pemesan.")


# =====================================
# 3. CETAK TIKET
# =====================================
st.write("---")
st.subheader("🎫 Cetak Tiket")

if "info_cetak" not in st.session_state:
    st.session_state.info_cetak = None

nama_cetak = st.text_input("Masukkan nama pemesan yang akan dicetak")

if st.button("Cetak Tiket"):
    hasil = st.session_state.tiket.cetak_tiket(nama_cetak)

    if hasil:
        st.session_state.info_cetak = {
            "kode_tiket": hasil.kode_tiket,
            "nama": hasil.nama,
            "alamat": hasil.alamat,
            "email": hasil.email,
            "no_telp": hasil.no_telp,
            "tanggal_lahir": hasil.tanggal_lahir,
            "kategori": hasil.kategori,
            "jumlah": hasil.jumlah,
            "pembayaran": hasil.pembayaran,
            "total": hasil.total
        }
        st.success("✅ Tiket berhasil dicetak!")
        st.rerun() # Refresh halaman agar status tabel di atas langsung berubah
    else:
        st.session_state.info_cetak = None
        st.error("❌ Data tidak ditemukan")

if st.session_state.info_cetak:
    t = st.session_state.info_cetak
    st.write("---")
    st.write("## 🎟 TIKET KONSER JUSTIN BIEBER")
    st.info(f"### KODE TIKET : {t['kode_tiket']}")
    st.write(f"**Nama Pemesan** : {t['nama']}")
    st.write(f"**Alamat** : {t['alamat']}")
    st.write(f"**Email** : {t['email']}")
    st.write(f"**No Telepon** : {t['no_telp']}")
    st.write(f"**Tanggal Lahir** : {t['tanggal_lahir']}")
    st.write(f"**Kategori Tiket** : {t['kategori']}")
    st.write(f"**Jumlah Tiket** : {t['jumlah']}")
    st.write(f"**Metode Pembayaran** : {t['pembayaran']}")
    st.write(f"**Total Harga** : Rp {t['total']:,}")
    st.success("🎉 Selamat Menikmati Konser Justin Bieber 🎉")


# =====================================
# 4. CARI PEMESAN (BY NO TELEPON)
# =====================================
st.write("---")
st.subheader("🔍 Cari Pemesan (Berdasarkan No. Telepon)")
telp_cari = st.text_input("Masukkan nomor telepon pemesan yang dicari")

if st.button("Cari Pemesan"):
    hasil = st.session_state.tiket.cari_by_telp(telp_cari)

    if hasil:
        st.success("✅ Data ditemukan")
        st.write(f"Kode Tiket : **{hasil.kode_tiket}**")
        st.write(f"Nama : {hasil.nama}")
        st.write(f"Alamat : {hasil.alamat}")
        st.write(f"Email : {hasil.email}")
        st.write(f"No Telepon : {hasil.no_telp}")
        st.write(f"Tanggal Lahir : {hasil.tanggal_lahir}")
        st.write(f"Kategori : {hasil.kategori}")
        st.write(f"Harga Tiket : Rp {hasil.harga:,}")
        st.write(f"Jumlah Tiket : {hasil.jumlah}")
        st.write(f"Total Harga : Rp {hasil.total:,}")
        st.write(f"Metode Pembayaran : {hasil.pembayaran}")
        st.write(f"Status Cetak : {hasil.status_cetak}")
    else:
        st.error("❌ Data dengan nomor telepon tersebut tidak ditemukan")


# =====================================
# 5. HAPUS PEMESAN
# =====================================
st.write("---")
st.subheader("🗑 Hapus Pemesan")
nama_hapus = st.text_input("Masukkan nama pemesan yang akan dihapus")

if st.button("Hapus Pemesan"):
    berhasil = st.session_state.tiket.hapus(nama_hapus)

    if berhasil:
        st.success(f"✅ Data {nama_hapus} berhasil dihapus")
        st.rerun()
    else:
        st.error("❌ Data tidak ditemukan")
