import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='whitegrid')

st.set_page_config(page_title="Analisis Penyewaan Sepeda", page_icon="🚲")
st.title('Analisis Pola Penyewaan Sepeda di Bengkulu. 🚲')
st.markdown('Oleh: Cadila Septi Natalia Panjaitan | ML')

# Memuat data dari file CSV
data_harian = pd.read_csv("data/day.csv")
data_perjam = pd.read_csv("data/hour.csv")

# Menghitung distribusi pengguna berdasarkan hari kerja dan libur
distribusi_hari_kerja = data_harian['workingday'].value_counts()
distribusi_hari_libur = data_harian['holiday'].value_counts()
distribusi_jam_kerja = data_perjam['workingday'].value_counts()
distribusi_jam_libur = data_perjam['holiday'].value_counts()

# Menghitung total pengguna untuk setiap kategori
total_pengguna_hari_kerja = distribusi_hari_kerja.sum()
total_pengguna_hari_libur = distribusi_hari_libur.sum()
total_pengguna_jam_kerja = distribusi_jam_kerja.sum()
total_pengguna_jam_libur = distribusi_jam_libur.sum()

st.subheader('Analisis Pola Penggunaan Sepeda (Data Harian)')

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pola Penyewaan Sepeda Seiring Waktu")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=data_harian, x='dteday', y='cnt', hue='season', ax=ax)
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Tren Penyewaan Sepeda Berdasarkan Musim')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("Hubungan Antar Variabel")
    corr = data_harian[['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, fmt='.2f')
    ax.set_title('Heatmap Korelasi Variabel')
    st.pyplot(fig)

st.subheader('Analisis Penggunaan Sepeda (Data Per Jam)')
col1, col2 = st.columns(2)

with col1:
    st.metric("Jumlah Pengguna pada Hari Kerja", value=total_pengguna_jam_kerja)
    fig, ax = plt.subplots()
    sns.barplot(x=distribusi_jam_kerja.index, y=distribusi_jam_kerja.values, ax=ax)
    ax.set_xlabel('Hari Kerja')
    ax.set_ylabel('Jumlah Pengguna')
    st.pyplot(fig)

with col2:
    st.metric("Jumlah Pengguna pada Hari Libur", value=total_pengguna_jam_libur)
    fig, ax = plt.subplots()
    sns.barplot(x=distribusi_jam_libur.index, y=distribusi_jam_libur.values, ax=ax)
    ax.set_xlabel('Hari Libur')
    ax.set_ylabel('Jumlah Pengguna')
    st.pyplot(fig)

st.markdown("---")
st.subheader("Analisis Jumlah Penyewaan Sepeda")

rental_count_workingdays = data_harian.groupby("workingday")["cnt"].sum()
rental_count_holiday = data_harian.groupby("holiday")["cnt"].sum()
rental_count_workinghour = data_perjam.groupby("workingday")["cnt"].sum()
rental_count_holihour = data_perjam.groupby("holiday")["cnt"].sum()

total_rental_workingday = rental_count_workingdays.sum()
total_rental_holiday = rental_count_holiday.sum()
total_rental_workinghour = rental_count_workinghour.sum()
total_rental_holihour = rental_count_holihour.sum()

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Penyewaan pada Hari Kerja", value=total_rental_workingday)
    fig, ax = plt.subplots()
    sns.barplot(x=rental_count_workingdays.index, y=rental_count_workingdays.values, ax=ax)
    ax.set_xlabel('Hari Kerja')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

with col2:
    st.metric("Total Penyewaan pada Hari Libur", value=total_rental_holiday)
    fig, ax = plt.subplots()
    sns.barplot(x=rental_count_holiday.index, y=rental_count_holiday.values, ax=ax)
    ax.set_xlabel('Hari Libur')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

st.markdown("---")
st.subheader("Analisis Pengaruh Cuaca terhadap Penyewaan Sepeda")

dataset_choice = st.selectbox("Pilih Dataset", ["Data Harian", "Data Per Jam"])

if dataset_choice == "Data Harian":
    data = data_harian
else:
    data = data_perjam

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(data['temp'], data['cnt'], c=data['weathersit'], cmap='viridis', alpha=0.6)
ax.set_xlabel('Temperatur')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_title('Pengaruh Temperatur dan Cuaca terhadap Penyewaan Sepeda')
legend1 = ax.legend(*scatter.legend_elements(), title="Kondisi Cuaca")
ax.add_artist(legend1)
st.pyplot(fig)

st.write("""
Scatter plot di atas menunjukkan hubungan antara temperatur, kondisi cuaca, dan jumlah penyewaan sepeda.
Setiap titik mewakili satu hari/jam, dengan warna menunjukkan kondisi cuaca.
Dari plot ini, kita dapat melihat bagaimana temperatur dan cuaca mempengaruhi tingkat penyewaan sepeda.
""")

st.subheader("Perbandingan Penyewaan: Hari Kerja vs Hari Libur")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=data_harian, x='workingday', y='cnt', ax=ax)
ax.set_xlabel('Hari Kerja (0: Libur, 1: Kerja)')
ax.set_ylabel('Jumlah Penyewaan')
st.pyplot(fig)

st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=data_harian, x='weathersit', y='cnt', ax=ax)
ax.set_xlabel('Kondisi Cuaca')
ax.set_ylabel('Jumlah Penyewaan')
ax.set_xticklabels(['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat'])
st.pyplot(fig)

st.markdown("---")
st.subheader("Kesimpulan")
st.markdown("""
    Berdasarkan analisis di atas, kita dapat menyimpulkan bahwa:
    1. Penyewaan sepeda memiliki pola musiman yang jelas.
    2. Hari kerja cenderung memiliki jumlah penyewaan yang lebih tinggi dibandingkan hari libur.
    3. Suhu memiliki korelasi positif yang kuat dengan jumlah penyewaan.
    4. Cuaca yang cerah dan berawan cenderung meningkatkan jumlah penyewaan sepeda.
""")