import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data dari main_data.csv
main_data_df = pd.read_csv('main_data.csv')  # Ganti dengan path yang sesuai


# Judul dashboard
st.title("E-Commerce Dashboard")

# Mengubah kolom timestamp ke format datetime
main_data_df['order_purchase_timestamp'] = pd.to_datetime(main_data_df['order_purchase_timestamp'])
main_data_df['year'] = main_data_df['order_purchase_timestamp'].dt.year

# Sidebar untuk filter tahun
years = main_data_df['year'].unique()
selected_year = st.sidebar.selectbox('Pilih Tahun', sorted(years))

# Menghitung total penjualan per kategori produk
filtered_data = main_data_df[main_data_df['year'] == selected_year]
sales_per_category = filtered_data.groupby('product_category_name').agg(total_sales=('order_id', 'count')).reset_index()

# Pertanyaan 1: Produk apa yang paling laris setiap tahunnya?
st.subheader('Produk Terlaris Tahun {}'.format(selected_year))
top_products = sales_per_category.sort_values(by='total_sales', ascending=False).head(10)
st.bar_chart(top_products.set_index('product_category_name'))

# Pertanyaan 2: Metode pembayaran yang paling sering digunakan
payment_summary = main_data_df.groupby('payment_type').agg(
    frequency=('order_id', 'count'),
    average_order_value=('payment_value', 'mean')
).reset_index()

st.subheader('Ringkasan Metode Pembayaran')
st.write(payment_summary)

# Visualisasi frekuensi metode pembayaran
st.subheader('Frekuensi Metode Pembayaran')
fig, ax = plt.subplots()
sns.barplot(data=payment_summary, x='payment_type', y='frequency', ax=ax, color='lightblue')
ax.set_title('Frekuensi Metode Pembayaran')
st.pyplot(fig)

# Pertanyaan 3: Rata-rata skor ulasan kategori produk terlaris
st.subheader('Rata-rata Skor Ulasan Kategori Produk Terlaris Tahun {}'.format(selected_year))
top_categories = top_products['product_category_name']  # Kategori produk terlaris
filtered_reviews = main_data_df[main_data_df['product_category_name'].isin(top_categories)]
category_review_scores = filtered_reviews.groupby('product_category_name')['review_score'].mean().reset_index(name='average_review_score')
st.bar_chart(category_review_scores.set_index('product_category_name'))

# Pertanyaan 4: Jumlah total pesanan tiap tahunnya
annual_orders = main_data_df.groupby(main_data_df['year']).size().reset_index(name='total_orders')
st.subheader('Jumlah Total Pesanan per Tahun')
st.bar_chart(annual_orders.set_index('year'))
