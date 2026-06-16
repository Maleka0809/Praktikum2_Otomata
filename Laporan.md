# Laporan Praktikum 2 Otomata

 
|  Nama | NRP  |    
|---|---|
| Maleka Ghaniya  | 5025241189  |   
| Jorell Ramos Sinaga  |  5025241202 |   
|  Angela Vania Sugiyono |  5025241224  |  

## Soal
Buatlah sebuah program untuk mengotomasi mesin PDA. Rancanglah user interface sedemikian hingga pengguna dapat mudah menginputkan string yang akan dibaca dan ditentukan keanggotaannya (Accepted atau Rejected) oleh mesin PDA tsb.

## Penjelasan 

![](https://github.com/Maleka0809/Praktikum2_Otomata/blob/main/Visual/PDA.png)

Mesin PDA yang digunakan pada praktikum ini adalah jenis **Deterministic Pushdown Automaton (DPDA)** yang dirancang untuk mengenali bahasa Context-Free Language:

$$L = \{ a^n b^n \mid n \ge 0 \}$$

Secara konsep, mesin ini bekerja dalam tiga fase utama:
1. **Fase Pushing (`'a'`)**: Ketika membaca karakter `'a'` pada state `READ 1`, mesin akan melakukan transisi menuju `PUSH a` untuk memasukkan karakter `'a'` ke dalam stack, kemudian berputar kembali ke `READ 1`.
2. **Fase Popping (`'b'`)**: Ketika membaca karakter `'b'` pada state `READ 1` atau `READ 2`, mesin akan beralih ke state `POP 1` untuk mengeluarkan satu karakter `'a'` dari stack sebagai pasangan pencocokan. Jika stack kosong saat di-pop sebelum pita habis, mesin langsung menuju `REJECT`.
3. **Fase Pemeriksaan Akhir ($\lambda$)**: Ketika seluruh pita input telah selesai dibaca (mencapai $\lambda$), mesin akan berpindah ke `POP 2` untuk memeriksa stack. Jika stack kosong (pop menghasilkan $\lambda$), maka jumlah `'a'` dan `'b'` terbukti sama, sehingga mesin menuju **ACCEPT**. Jika masih ada karakter tersisa di stack, mesin menuju **REJECT**.

## Penjelasan Kode

Kode program diimplementasikan menggunakan bahasa pemrograman Python dengan antarmuka grafis modern memanfaatkan pustaka **CustomTkinter**. Arsitektur kode dibagi menjadi dua komponen utama:

1. **Kelas `PDASimulator` (Logika)**:
   * Mengatur logika internal mesin PDA (pita input, stack, dan pencatatan riwayat transisi langkah demi langkah).
   * Fungsi `step()` menjalankan satu langkah transisi berdasarkan *state* aktif saat ini (`READ_1`, `PUSH_a`, `POP_1`, `READ_2`, `POP_2`, `ACCEPT`, `REJECT`), memperbarui isi tumpukan, sisa pita, dan mengembalikan status keaktifan.

2. **Kelas `PDAGUI` (Tampilan)**:
   * Mengatur tata letak antarmuka grafis (GUI) yang interaktif.
   * **Flowchart Canvas**: Menggambar node diagram dan panah transisi secara dinamis dan menyorot node/jalur transisi aktif saat simulasi berjalan.
   * **Visualisasi Pita & Stack**: Menggambar isi tumpukan stack secara vertikal dan sisa pita input secara horizontal lengkap dengan petunjuk pembacaan *tape head*.
   * **Kontrol Simulasi**: Menyediakan tombol interaktif seperti *Mulai Simulasi*, *Auto Play*, *Simulasi Instan*, dan *Reset*.
   * **Log Transisi**: Menampilkan riwayat langkah mesin PDA secara mendetail dalam kotak teks log.

## Cara Menjalankan

1. Pastikan `customtkinter` telah terinstal. Jika belum, instal lewat terminal:
   ```bash
   pip install customtkinter
   ```
2. Jalankan berkas program menggunakan python:
   ```bash
   python praktikum2.py
   ```
