import streamlit as st
from collections import deque

# =========================
# KELAS ANTRIAN PUSKESMAS
# =========================
class PuskesmasQueue:
    def __init__(self):
        self.darurat_queue = deque()
        self.lansia_queue = deque()
        self.ibu_hamil_queue = deque()
        self.umum_queue = deque()
        self.counter = 0

    def ambil_nomor(self, nama, kategori):
        self.counter += 1

        pasien = {
            "nomor": self.counter,
            "nama": nama,
            "kategori": kategori
        }

        if kategori == "Darurat":
            self.darurat_queue.append(pasien)

        elif kategori == "Lansia":
            self.lansia_queue.append(pasien)

        elif kategori == "Ibu Hamil":
            self.ibu_hamil_queue.append(pasien)

        else:
            self.umum_queue.append(pasien)

        return self.counter

    def panggil_pasien(self):

        if self.darurat_queue:
            return self.darurat_queue.popleft()

        elif self.lansia_queue:
            return self.lansia_queue.popleft()

        elif self.ibu_hamil_queue:
            return self.ibu_hamil_queue.popleft()

        elif self.umum_queue:
            return self.umum_queue.popleft()

        return None

    def get_queues(self):
        return (
            list(self.darurat_queue),
            list(self.lansia_queue),
            list(self.ibu_hamil_queue),
            list(self.umum_queue)
        )


# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Antrean Puskesmas",
    layout="wide"
)

st.title("🏥 Sistem Antrean Puskesmas")
st.subheader("Priority Queue")

# =========================
# SESSION STATE
# =========================
if "puskesmas" not in st.session_state:
    st.session_state.puskesmas = PuskesmasQueue()

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.header("📝 Pendaftaran Pasien")

    nama = st.text_input("Nama Pasien")

    kategori = st.selectbox(
        "Kategori Pasien",
        [
            "Umum",
            "Ibu Hamil",
            "Lansia",
            "Darurat"
        ]
    )

    if st.button("Ambil Nomor Antrean",
                 use_container_width=True):

        if nama:

            nomor = (
                st.session_state.puskesmas
                .ambil_nomor(nama, kategori)
            )

            st.success(
                f"Nomor antrean Anda: {nomor}"
            )

            st.rerun()

        else:
            st.warning("Masukkan nama pasien!")

# =========================
# TAMPILKAN ANTREAN
# =========================
darurat, lansia, ibu_hamil, umum = (
    st.session_state.puskesmas.get_queues()
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("🚑 Antrean Darurat")

    if darurat:
        for pasien in darurat:
            st.error(
                f"No {pasien['nomor']} - {pasien['nama']}"
            )
    else:
        st.write("Kosong")

    st.subheader("👴 Antrean Lansia")

    if lansia:
        for pasien in lansia:
            st.warning(
                f"No {pasien['nomor']} - {pasien['nama']}"
            )
    else:
        st.write("Kosong")

with col2:

    st.subheader("🤰 Antrean Ibu Hamil")

    if ibu_hamil:
        for pasien in ibu_hamil:
            st.info(
                f"No {pasien['nomor']} - {pasien['nama']}"
            )
    else:
        st.write("Kosong")

    st.subheader("👤 Antrean Umum")

    if umum:
        for pasien in umum:
            st.success(
                f"No {pasien['nomor']} - {pasien['nama']}"
            )
    else:
        st.write("Kosong")

# =========================
# PANGGIL PASIEN
# =========================
st.markdown("---")
st.subheader("📢 Panggil Pasien")

if st.button(
    "Panggil Pasien Berikutnya",
    use_container_width=True
):

    pasien = (
        st.session_state.puskesmas
        .panggil_pasien()
    )

    if pasien:

        st.success(
            f"Nomor {pasien['nomor']} - "
            f"{pasien['nama']} "
            f"({pasien['kategori']}) "
            f"silakan menuju ruang pemeriksaan."
        )

        st.balloons()
        st.rerun()

    else:
        st.warning("Tidak ada pasien dalam antrean.")
