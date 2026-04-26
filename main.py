import pickle
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/articles_metadata.csv")
    tfidf_matrix = pickle.load(open("model/tfidf_matrix.pkl", "rb"))
    vectorizer = pickle.load(open("model/tfidf_vectorizer.pkl", "rb"))
    return df, tfidf_matrix, vectorizer

def search(query, vectorizer, tfidf_matrix, df, threshold=0.1):
    q_vec = vectorizer.transform([query])
    scores = cosine_similarity(q_vec, tfidf_matrix)[0]
    
    hasil = []
    for i, score in enumerate(scores):
        if score >= threshold:
            hasil.append({'score': score, 'index': i})
    
    hasil.sort(key=lambda x: x['score'], reverse=True)
    return df.iloc[[h['index'] for h in hasil]].assign(score=[h['score'] for h in hasil])

# Main app
st.set_page_config(page_title="Search Engine", page_icon="🔍")

st.title("🔍 Search Engine")
st.markdown("Cari artikel berita dan informasi")

with st.spinner("Loading search engine..."):
    df, tfidf_matrix, vectorizer = load_data()

with st.sidebar:
    st.header("Pengaturan")
    threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.1, 0.05)
    st.info(f"Total artikel: {len(df)}")

query = st.text_input("Masukkan kata kunci pencarian:", placeholder="Contoh: politik, pendidikan, hukum...")

if query:
    with st.spinner("Mencari..."):
        results = search(query, vectorizer, tfidf_matrix, df, threshold)
    
    if len(results) == 0:
        st.warning(f"Tidak ada hasil dengan similarity ≥ {threshold}")
    else:
        st.success(f"Ditemukan {len(results)} hasil")
        
        # Pagination dengan selectbox
        items_per_page = 10
        total_pages = (len(results) - 1) // items_per_page + 1
        
        page = st.selectbox(
            "Pilih Halaman",
            options=range(1, total_pages + 1),
            format_func=lambda x: f"Halaman {x}"
        )
        
        start = (page - 1) * items_per_page
        end = start + items_per_page
        
        st.caption(f"Menampilkan hasil {start + 1} - {min(end, len(results))} dari {len(results)}")
        
        for idx, row in results.iloc[start:end].iterrows():
            with st.container():
                st.markdown(f"### 📄 {row['judul']}")
                st.markdown(f"**Kategori:** `{row['kategori']}` | **Similarity:** {row['score']:.2%}")
                
                preview = str(row['isi'])[:200] + "..." if len(str(row['isi'])) > 200 else str(row['isi'])
                st.markdown(f"**Preview:** {preview}")
                
                col1, col2 = st.columns(2)
                with col1:
                    with st.expander("📖 Baca Selengkapnya (Metadata)"):
                        st.write(row['isi'])
                with col2:
                    st.markdown(f"🔗 [Baca Selengkapnya di Website Asli]({row['link']})")
                
                st.markdown("---")
else:
    st.info("💡 Masukkan kata kunci untuk memulai pencarian")

st.markdown("---")
st.markdown("<center>Search Engine | TF-IDF + Cosine Similarity</center>", unsafe_allow_html=True)