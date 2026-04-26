Berikut adalah **README.md** yang lengkap, detail, dan mudah dipahami oleh pemula sekalipun. Saya akan menjelaskan struktur proyek, fungsi setiap file, dan setiap baris kode secara rinci.

```markdown
# 🔍 Detik.com Search Engine

Proyek ini adalah **mesin pencari sederhana** untuk artikel berita dari **Detik.com**. Pengguna bisa mencari artikel berdasarkan kata kunci, dan sistem akan menampilkan artikel yang paling relevan menggunakan metode **TF-IDF** dan **Cosine Similarity**.

---

## 📁 Struktur Proyek

```
.
├── data
│   └── articles_metadata.csv      # Hasil akhir: metadata artikel (judul, link, kategori)
├── main.py                         # Aplikasi utama (Streamlit web app)
├── model
│   ├── tfidf_matrix.pkl            # File model TF-IDF (matrix sparce)
│   └── tfidf_vectorizer.pkl        # Vectorizer untuk mengubah teks → vektor TF-IDF
├── notebook
│   ├── crawling-ferischa.ipynb     # Notebook untuk crawling artikel dari Detik.com
│   └── preprocessing-ferischa.ipynb # Notebook untuk preprocessing + TF-IDF
└── requirements.txt                # Daftar library yang diperlukan
```

---

## 🧠 Apa Itu TF-IDF dan Cosine Similarity?

| Istilah | Penjelasan Sederhana |
|---------|----------------------|
| **TF-IDF** | Teknik mengubah teks menjadi angka-angka (vektor) berdasarkan seberapa penting suatu kata dalam dokumen. |
| **Cosine Similarity** | Mengukur seberapa mirip dua vektor (kata kunci pencarian vs artikel). Nilai 0 = tidak mirip, 1 = sangat mirip. |

---

## 📦 Requirements (library yang digunakan)

Buat file `requirements.txt` dengan isi:

```txt
streamlit
pandas
scikit-learn
Sastrawi
requests
beautifulsoup4
```

Cara install:
```bash
pip install -r requirements.txt
```

---

## 🕷️ 1. Crawling (Mengambil Artikel dari Detik.com)

**File:** `notebook/crawling-ferischa.ipynb`

### 📌 Tujuan
Mengambil artikel berita dari berbagai kategori di Detik.com secara acak hingga terkumpul 1260 artikel.

### 📌 Penjelasan Kode Per Baris

| Baris | Kode | Kegunaan |
|-------|------|----------|
| 1-3 | `import requests, BeautifulSoup, pandas, time, random` | Library untuk request HTTP, parsing HTML, manipulasi data, jeda waktu, dan acak. |
| 8 | `HEADERS = {"User-Agent": "Mozilla/5.0"}` | Header agar server mengira kita adalah browser normal. |
| 10-18 | `base_urls = [...]` | Daftar URL kategori Detik.com (Ekonomi, Politik, Teknologi, dll). |
| 20 | `categories = [...]` | Nama kategori yang sesuai dengan URL. |
| 26-44 | `def crawl_detik_content(link):` | Fungsi untuk mengambil isi artikel dari link. |
| 28-29 | `requests.get(link, headers=HEADERS, timeout=10)` | Mengirim request ke halaman artikel. |
| 31-32 | `BeautifulSoup(resp.text, "html.parser")` | Parsing HTML. |
| 34-35 | `soup.find("div", class_="detail__body-text")` | Mencari div yang berisi teks artikel di Detik. |
| 38-40 | `find_all("p")` | Mengambil semua paragraf dan menggabungkannya. |
| 49-90 | `def crawl_detik_random_total(...)` | Fungsi utama crawling. |
| 55 | `random.shuffle(combined)` | Mengacak urutan kategori agar seimbang. |
| 62-64 | Looping `for page in range(1, max_page+1)` | Looping setiap halaman dalam kategori. |
| 66-68 | `requests.get(url)` | Mengambil daftar artikel di halaman tersebut. |
| 72-73 | `soup.find_all("article")` | Mencari semua tag `<article>` yang berisi ringkasan artikel. |
| 79-82 | `a_tag = art.find("a", href=True)` | Mengambil link artikel. |
| 86-87 | `judul_tag = art.find("h2")` | Mengambil judul artikel. |
| 89 | `crawl_detik_content(link)` | Ambil isi lengkap artikel. |
| 92-98 | `data.append(...)` | Simpan judul, link, isi, dan kategori. |
| 107-108 | `time.sleep(0.3)` | Jeda 0.3 detik agar tidak membebani server. |
| 124-128 | `df.drop_duplicates()` dan `df.sample(n=1260)` | Hapus duplikat dan ambil 1260 artikel secara acak. |
| 130 | `df_final.to_csv(...)` | Simpan ke file CSV. |

---

## 🧹 2. Preprocessing dan TF-IDF

**File:** `notebook/preprocessing-ferischa.ipynb`

### 📌 Tujuan
Membersihkan teks artikel (lowercase, hapus tanda baca, hapus kata tidak penting, stemming) lalu mengubahnya menjadi vektor TF-IDF.

### 📌 Penjelasan Kode Per Baris

| Baris | Kode | Kegunaan |
|-------|------|----------|
| 1-2 | `!pip install Sastrawi scikit-learn` | Install library stemming dan TF-IDF (jika di notebook). |
| 6-11 | Import library | Pandas (data), re (regex), pickle (simpan model), Sastrawi (stopword & stemmer), sklearn (TF-IDF). |
| 15 | `path = "/kaggle/input/..."` | Lokasi file hasil crawling. |
| 18 | `df = pd.read_csv(path)` | Baca CSV ke DataFrame. |
| 23-24 | `StopWordRemoverFactory()` dan `get_stop_words()` | Mengambil daftar kata tidak penting (contoh: "yang", "dan", "di"). |
| 26-27 | `StemmerFactory()` dan `create_stemmer()` | Membuat stemmer untuk mengubah kata ke bentuk dasar (contoh: "mencari" → "cari"). |
| 32-44 | `def preprocess_text(text):` | Fungsi utama preprocessing. |
| 35 | `text.lower()` | Ubah huruf besar jadi kecil. |
| 36 | `re.sub(r"http\S+", " ", text)` | Hapus link URL. |
| 37 | `re.sub(r"[^a-z\s]", " ", text)` | Hanya huruf a-z dan spasi (hapus angka, tanda baca). |
| 38 | `re.sub(r"\s+", " ", text).strip()` | Hapus spasi berlebih. |
| 41 | `[t for t in tokens if t not in stopwords]` | Hapus kata tidak penting. |
| 42 | `[stemmer.stem(t) for t in tokens]` | Stemming setiap kata. |
| 48-49 | `df["isi_clean"]` dan `df["judul_clean"]` apply preprocessing | Bersihkan isi dan judul artikel. |
| 50 | `df["text_clean"] = judul_clean + " " + isi_clean` | Gabungkan judul dan isi untuk pencarian lebih akurat. |
| 55 | `TfidfVectorizer(max_features=5000)` | Buat vectorizer dengan maksimal 5000 kata unik. |
| 57 | `vectorizer.fit_transform(df["text_clean"])` | Ubah teks menjadi matriks TF-IDF. |
| 60 | `print("TF-IDF shape:", tfidf_matrix.shape)` | Contoh: (1260, 5000) = 1260 artikel, 5000 fitur kata. |
| 65-66 | `df[["judul", "link", "kategori"]].to_csv(...)` | Simpan metadata (tanpa teks bersih/vektor). |
| 70-71 | `pickle.dump(tfidf_matrix, file)` | Simpan matriks TF-IDF (format sparce). |
| 74-75 | `pickle.dump(vectorizer, file)` | Simpan vectorizer untuk dipakai di main.py. |

---

## 🚀 3. Aplikasi Search Engine (main.py)

**File:** `main.py` (aplikasi Streamlit)

### 📌 Tujuan
Membuat antarmuka web tempat pengguna bisa mengetik kata kunci dan mendapatkan artikel relevan.

### 📌 Penjelasan Kode Per Baris

| Baris | Kode | Kegunaan |
|-------|------|----------|
| 1-5 | Import library | pickle (load model), pandas (data), streamlit (UI), cosine_similarity (hitungan kemiripan). |
| 8-13 | `@st.cache_data` dan `def load_data():` | Cache agar data tidak dimuat ulang setiap interaksi. |
| 9 | `pd.read_csv("data/articles_metadata.csv")` | Baca metadata artikel. |
| 10-11 | `pickle.load(open(...))` | Load TF-IDF matrix dan vectorizer. |
| 15-26 | `def search(query, vectorizer, tfidf_matrix, df, threshold=0.1):` | Fungsi pencarian. |
| 16 | `q_vec = vectorizer.transform([query])` | Ubah kata kunci pengguna menjadi vektor TF-IDF. |
| 17 | `cosine_similarity(q_vec, tfidf_matrix)[0]` | Hitung kemiripan dengan semua artikel. Hasil: array skor 0-1. |
| 19-23 | Looping `for i, score in enumerate(scores):` | Kumpulkan artikel dengan skor >= threshold. |
| 25 | `sort(key=lambda x: x['score'], reverse=True)` | Urutkan dari skor tertinggi ke terendah. |
| 26 | Kembalikan DataFrame yang sudah difilter dan ditambah kolom `score`. |
| 30 | `st.set_page_config(...)` | Set judul tab browser dan ikon. |
| 32-33 | `st.title()` dan `st.markdown()` | Tampilkan judul besar dan deskripsi. |
| 35-36 | `with st.spinner(...):` | Tampilkan animasi loading saat load data. |
| 39-43 | `with st.sidebar:` | Buat sidebar untuk pengaturan. |
| 40 | `st.slider("Similarity Threshold", 0.0, 1.0, 0.1)` | Slider untuk mengatur batas minimal kemiripan. |
| 41 | `st.info(f"Total artikel: {len(df)}")` | Tampilkan jumlah artikel. |
| 45 | `st.text_input(...)` | Kotak input teks untuk kata kunci pencarian. |
| 47-88 | `if query:` | Jika pengguna sudah mengetik sesuatu. |
| 49-50 | `with st.spinner("Mencari..."):` dan `results = search(...)` | Jalankan pencarian. |
| 52-53 | `if len(results) == 0:` | Jika tidak ada hasil yang memenuhi threshold. |
| 56 | `st.success(f"Ditemukan {len(results)} hasil")` | Tampilkan jumlah hasil. |
| 59-60 | `items_per_page = 10` dan `total_pages = ...` | Pagination: 10 hasil per halaman. |
| 62-65 | `st.selectbox("Pilih Halaman", ...)` | Dropdown untuk pindah halaman. |
| 67-68 | `start = (page-1) * 10`, `end = start + 10` | Hitung indeks awal dan akhir. |
| 72-86 | Looping `for idx, row in results.iloc[start:end].iterrows():` | Tampilkan setiap hasil. |
| 73 | `st.markdown(f"### 📄 {row['judul']}")` | Judul artikel (heading level 3). |
| 74 | `st.markdown(f"**Kategori:** ...")` | Tampilkan kategori dan skor similarity. |
| 76-77 | `preview = str(row['isi'])[:200] + "..."` | Potongan awal artikel (200 karakter). |
| 79-84 | `st.expander()` dan `st.markdown(f"🔗 [Link]({row['link']})")` | Expander untuk baca lengkap + link ke artikel asli. |
| 90 | `st.info("💡 Masukkan kata kunci...")` | Pesan saat belum ada pencarian. |
| 93-94 | `st.markdown("---")` dan footer | Garis pemisah dan kredit. |

---

## 🖥️ Cara Menjalankan Aplikasi

### 1. Clone atau buat folder proyek dengan struktur di atas

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan crawling (jika belum punya data)
Buka `notebook/crawling-ferischa.ipynb` dan jalankan semua sel.  
Atau jalankan sebagai script Python.

### 4. Jalankan preprocessing
Buka `notebook/preprocessing-ferischa.ipynb` dan jalankan semua sel.  
Pastikan file hasil crawling berada di path yang benar.

### 5. Jalankan aplikasi Streamlit
```bash
streamlit run main.py
```

Aplikasi akan terbuka di browser (biasanya `http://localhost:8501`).

---

## 📝 Catatan Penting

- **Threshold** mengatur seberapa ketat pencarian. Nilai 0.1 berarti artikel dengan kemiripan ≥10% akan ditampilkan.
- **Pagination** membantu jika hasil pencarian banyak (10 artikel per halaman).
- **Cache** pada `load_data()` membuat aplikasi tetap cepat meskipun pengguna mencari berkali-kali.
- File `tfidf_matrix.pkl` berformat **sparse matrix** (hemat memori karena banyak nilai 0).

---

## 🧪 Contoh Penggunaan

1. Ketik `"politik"` → akan menampilkan artikel tentang politik dengan skor similarity tinggi.
2. Ketik `"kesehatan virus"` → artikel tentang kesehatan yang mengandung kata "virus".
3. Geser slider threshold ke `0.05` → hasil lebih banyak (tapi kurang relevan).

---

## 📚 Kesimpulan

| Komponen | Fungsi |
|----------|--------|
| Crawling | Mengumpulkan artikel dari Detik.com |
| Preprocessing | Membersihkan teks + stemming |
| TF-IDF | Mengubah teks ke vektor numerik |
| Cosine Similarity | Menghitung relevansi pencarian |
| Streamlit | Antarmuka web interaktif |

Dengan proyek ini, Anda bisa memahami alur lengkap **Information Retrieval System** dari pengambilan data hingga penyajian hasil pencarian.
```

---

README di atas sudah **lengkap dan mendetail**, mencakup:

1. **Penjelasan struktur proyek** - setiap folder dan file
2. **Penjelasan konsep** - TF-IDF dan Cosine Similarity dengan bahasa sederhana
3. **Penjelasan kode crawling** - baris per baris dengan tabel yang rapi
4. **Penjelasan kode preprocessing** - baris per baris dengan tabel
5. **Penjelasan main.py** - baris per baris dengan tabel
6. **Cara menjalankan** - langkah demi langkah
7. **Contoh penggunaan** - agar pengguna langsung paham
8. **Tabel kesimpulan** - ringkasan per komponen

Orang awam sekalipun akan bisa memahami tujuan setiap baris kode dan cara kerja keseluruhan sistem.