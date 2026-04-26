Berikut adalah **README.md** yang lebih rapi dan terstruktur dengan baik, bisa langsung Anda copy-paste ke file `README.md`:

```markdown
# 🔍 Detik.com Search Engine

Proyek mesin pencari artikel berita dari Detik.com menggunakan **TF-IDF** + **Cosine Similarity** dengan antarmuka **Streamlit**.

---

## 📁 Struktur Proyek

```
.
├── data
│   └── articles_metadata.csv      # Metadata artikel (judul, link, kategori)
├── main.py                         # Aplikasi Streamlit (frontend + search engine)
├── model
│   ├── tfidf_matrix.pkl            # Matriks TF-IDF (format sparse)
│   └── tfidf_vectorizer.pkl        # Vectorizer untuk konversi teks
├── notebook
│   ├── crawling-ferischa.ipynb     # Crawling artikel dari Detik.com
│   └── preprocessing-ferischa.ipynb # Preprocessing + pembuatan model TF-IDF
└── requirements.txt                # Daftar dependency
```

---

## 🧠 Konsep Dasar

| Istilah | Penjelasan |
|---------|------------|
| **TF-IDF** | Mengubah teks menjadi vektor angka berdasarkan pentingnya kata dalam dokumen |
| **Cosine Similarity** | Mengukur kemiripan antara dua vektor (0 = tidak mirip, 1 = sangat mirip) |
| **Stemming** | Mengubah kata ke bentuk dasar (contoh: "mencari" → "cari") |
| **Stopword** | Kata tidak penting yang dihapus ("yang", "dan", "di") |

---

## 📦 Dependencies (requirements.txt)

```txt
streamlit
pandas
scikit-learn
Sastrawi
requests
beautifulsoup4
```

**Install dengan perintah:**
```bash
pip install -r requirements.txt
```

---

## 🕷️ 1. Crawling Artikel

**File:** `notebook/crawling-ferischa.ipynb`

### Tujuan
Mengambil 1260 artikel berita dari 9 kategori Detik.com secara acak.

### Penjelasan Kode

| Baris | Kode | Fungsi |
|-------|------|--------|
| 1-5 | `import requests, BeautifulSoup, pandas, time, random` | Import library |
| 8 | `HEADERS = {"User-Agent": "Mozilla/5.0"}` | Header agar dianggap browser |
| 10-18 | `base_urls = [...]` | 9 URL kategori Detik.com |
| 20 | `categories = [...]` | Nama kategori (Economy, Politics, dll) |
| 26-44 | `def crawl_detik_content(link):` | Ambil isi artikel dari link |
| 28-29 | `requests.get(link, timeout=10)` | Request halaman artikel |
| 34-35 | `soup.find("div", class_="detail__body-text")` | Cari div konten artikel |
| 38-40 | `find_all("p")` | Ambil semua paragraf |
| 49-90 | `def crawl_detik_random_total(...):` | Fungsi utama crawling |
| 55 | `random.shuffle(combined)` | Acak urutan kategori |
| 62-64 | `for page in range(1, max_page+1):` | Looping setiap halaman |
| 72-73 | `soup.find_all("article")` | Cari semua artikel di halaman |
| 79-82 | `a_tag = art.find("a", href=True)` | Ambil link artikel |
| 86-87 | `judul_tag = art.find("h2")` | Ambil judul artikel |
| 92-98 | `data.append({...})` | Simpan ke list |
| 107-108 | `time.sleep(0.3)` | Jeda agar tidak ban server |
| 124-128 | `df.drop_duplicates()` + `df.sample(n=1260)` | Hapus duplikat & ambil 1260 acak |
| 130 | `df_final.to_csv(output_csv)` | Simpan ke CSV |

---

## 🧹 2. Preprocessing & TF-IDF

**File:** `notebook/preprocessing-ferischa.ipynb`

### Tujuan
Membersihkan teks, melakukan stemming, lalu mengubah ke vektor TF-IDF.

### Penjelasan Kode

| Baris | Kode | Fungsi |
|-------|------|--------|
| 1-2 | `!pip install Sastrawi scikit-learn` | Install library |
| 6-11 | Import library | Pandas, re, pickle, Sastrawi, sklearn |
| 15 | `path = ".../detik_random_1260.csv"` | Lokasi hasil crawling |
| 23-24 | `StopWordRemoverFactory()` | Buat objek stopword remover |
| 26-27 | `StemmerFactory()` + `create_stemmer()` | Buat objek stemmer |
| 32-44 | `def preprocess_text(text):` | Fungsi preprocessing |
| 35 | `text.lower()` | Lowercase semua huruf |
| 36 | `re.sub(r"http\S+", " ", text)` | Hapus URL |
| 37 | `re.sub(r"[^a-z\s]", " ", text)` | Hapus angka & tanda baca |
| 38 | `re.sub(r"\s+", " ", text).strip()` | Hapus spasi berlebih |
| 41 | `[t for t in tokens if t not in stopwords]` | Hapus stopword |
| 42 | `[stemmer.stem(t) for t in tokens]` | Stemming setiap kata |
| 48 | `df["isi_clean"] = df["isi"].apply(preprocess_text)` | Bersihkan isi artikel |
| 49 | `df["judul_clean"] = df["judul"].apply(preprocess_text)` | Bersihkan judul |
| 50 | `df["text_clean"] = df["judul_clean"] + " " + df["isi_clean"]` | Gabungkan judul & isi |
| 55 | `TfidfVectorizer(max_features=5000)` | Buat vectorizer (5000 kata unik) |
| 57 | `tfidf_matrix = vectorizer.fit_transform(df["text_clean"])` | Konversi ke matriks TF-IDF |
| 65-66 | `df[["judul","link","kategori"]].to_csv("articles_metadata.csv")` | Simpan metadata |
| 70-71 | `pickle.dump(tfidf_matrix, open("tfidf_matrix.pkl","wb"))` | Simpan matriks TF-IDF |
| 74-75 | `pickle.dump(vectorizer, open("tfidf_vectorizer.pkl","wb"))` | Simpan vectorizer |

---

## 🚀 3. Aplikasi Search Engine (main.py)

**File:** `main.py`

### Tujuan
Antarmuka web untuk pencarian artikel dengan Streamlit.

### Penjelasan Kode

| Baris | Kode | Fungsi |
|-------|------|--------|
| 1-5 | `import pickle, pandas, streamlit, cosine_similarity` | Import library |
| 8-13 | `@st.cache_data` + `def load_data():` | Load data dengan caching |
| 9 | `pd.read_csv("data/articles_metadata.csv")` | Baca metadata |
| 10-11 | `pickle.load(open("model/tfidf_matrix.pkl","rb"))` | Load matriks TF-IDF |
| 11 | `pickle.load(open("model/tfidf_vectorizer.pkl","rb"))` | Load vectorizer |
| 15-26 | `def search(query, vectorizer, tfidf_matrix, df, threshold=0.1):` | Fungsi pencarian |
| 16 | `q_vec = vectorizer.transform([query])` | Ubah query ke vektor TF-IDF |
| 17 | `scores = cosine_similarity(q_vec, tfidf_matrix)[0]` | Hitung kemiripan dengan semua artikel |
| 19-23 | `for i, score in enumerate(scores):` | Filter artikel ≥ threshold |
| 25 | `hasil.sort(key=lambda x: x['score'], reverse=True)` | Urutkan dari skor tertinggi |
| 30 | `st.set_page_config(page_title="Search Engine", page_icon="🔍")` | Konfigurasi halaman |
| 35-36 | `with st.spinner("Loading..."):` + `load_data()` | Load data dengan animasi |
| 39-43 | `with st.sidebar:` | Sidebar pengaturan |
| 40 | `threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.1)` | Slider threshold |
| 45 | `query = st.text_input("Masukkan kata kunci:")` | Input pencarian |
| 49-50 | `results = search(query, vectorizer, tfidf_matrix, df, threshold)` | Jalankan pencarian |
| 59-60 | `items_per_page = 10` + `total_pages = ...` | Pagination (10 per halaman) |
| 62-65 | `page = st.selectbox("Pilih Halaman", range(1,total_pages+1))` | Dropdown halaman |
| 72-86 | `for idx, row in results.iloc[start:end].iterrows():` | Looping hasil pencarian |
| 73 | `st.markdown(f"### 📄 {row['judul']}")` | Tampilkan judul |
| 74 | `st.markdown(f"**Kategori:** {row['kategori']} \| **Similarity:** {row['score']:.2%}")` | Tampilkan kategori & skor |
| 76-77 | `preview = str(row['isi'])[:200] + "..."` | Preview 200 karakter pertama |
| 79-84 | `st.expander("📖 Baca Selengkapnya")` + `st.markdown(f"🔗 [Link]({row['link']})")` | Baca lengkap & link asli |

---

## 🖥️ Cara Menjalankan

### Langkah 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Langkah 2: Crawling Data
```bash
# Buka dan jalankan notebook crawling-ferischa.ipynb
# Atau jalankan sebagai script Python
```

### Langkah 3: Preprocessing & Buat Model
```bash
# Buka dan jalankan notebook preprocessing-ferischa.ipynb
```

### Langkah 4: Jalankan Aplikasi
```bash
streamlit run main.py
```

Aplikasi akan terbuka di `http://localhost:8501`

---

## 🎮 Cara Penggunaan

| Langkah | Aksi |
|---------|------|
| 1 | Ketik kata kunci di kotak pencarian (contoh: "politik", "kesehatan", "teknologi") |
| 2 | Atur **Similarity Threshold** di sidebar (0.1 = 10% kemiripan ke atas) |
| 3 | Klik hasil pencarian untuk membaca preview |
| 4 | Klik "Baca Selengkapnya" untuk melihat isi penuh |
| 5 | Klik link untuk membuka artikel asli di Detik.com |

---

## 📊 Contoh Hasil Pencarian

| Query | Hasil |
|-------|-------|
| `"politik"` | Artikel tentang politik dengan skor similarity tinggi |
| `"kesehatan virus"` | Artikel kesehatan yang mengandung kata "virus" |
| `"pendidikan"` | Artikel seputar pendidikan |

**Tips:** Jika hasil terlalu sedikit, turunkan threshold (misal ke 0.05). Jika terlalu banyak, naikkan threshold (misal ke 0.3).

---

## 📝 Catatan Teknis

| Komponen | Detail |
|----------|--------|
| **Jumlah artikel** | 1260 artikel (bisa disesuaikan) |
| **Kategori** | 9 kategori (Ekonomi, Politik, Teknologi, Lifestyle, Olahraga, Kesehatan, Pendidikan, Lingkungan, Hukum) |
| **Max features TF-IDF** | 5000 kata unik |
| **Format matriks** | Sparse matrix (hemat memori) |
| **Threshold default** | 0.1 (10%) |
| **Pagination** | 10 hasil per halaman |

---

## 📚 Ringkasan Alur Proyek

```
1. Crawling          →  Mengambil artikel dari Detik.com (1260 artikel)
         ↓
2. Preprocessing     →  Bersihkan teks, hapus stopword, stemming
         ↓
3. TF-IDF           →  Ubah teks menjadi vektor angka
         ↓
4. Search Engine    →  Streamlit app dengan cosine similarity
```

---

## 👨‍💻 Dibuat dengan

- Python 3.x
- Streamlit (frontend)
- Scikit-learn (TF-IDF & Cosine Similarity)
- Sastrawi (Stemmer Bahasa Indonesia)
- BeautifulSoup4 (Crawling)
- Pandas (Manipulasi data)

---

**© 2024 - Proyek Information Retrieval System**
```

README ini sudah:
- ✅ Rapi dengan heading dan subheading yang jelas
- ✅ Menggunakan tabel untuk penjelasan kode per baris
- ✅ Ada emoji untuk visualisasi yang lebih menarik
- ✅ Ada diagram alur sederhana
- ✅ Penjelasan lengkap dari A sampai Z
- ✅ Cocok untuk pemula yang ingin memahami setiap bagian
