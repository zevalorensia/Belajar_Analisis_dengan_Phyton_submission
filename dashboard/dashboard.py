import pandas as pd
import streamlit as st

# Membaca data yang telah digabungkan
data = pd.read_csv('../data/main_data.csv')

# Pastikan kolom order_purchase_timestamp adalah datetime
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'], errors='coerce')

# Judul dashboard
st.title("E-Commerce Dashboard")

# Pertanyaan 1: Produk paling laris
st.subheader("Produk Paling Laris")
top_products = data['product_id'].value_counts().head(10)
st.bar_chart(top_products)

# Pertanyaan 2: Metode pembayaran yang sering digunakan
st.subheader("Metode Pembayaran yang Sering Digunakan")
payment_summary = data.groupby('payment_type').agg(
    frequency=('order_id', 'count'),
    average_order_value=('payment_value', 'mean')
).reset_index()
st.bar_chart(payment_summary.set_index('payment_type')['frequency'])

# Pertanyaan 3: Distribusi skor ulasan
st.subheader("Distribusi Skor Ulasan")
review_scores = data.groupby('product_id')['review_score'].mean().reset_index()
st.bar_chart(review_scores.set_index('product_id')['review_score'])

# Filter untuk memilih rentang tahun
st.subheader("Filter Rentang Tahun untuk Jumlah Total Pesanan")
start_year, end_year = st.slider(
    "Pilih rentang tahun:",
    min_value=data['order_purchase_timestamp'].dt.year.min(),
    max_value=data['order_purchase_timestamp'].dt.year.max(),
    value=(data['order_purchase_timestamp'].dt.year.min(), data['order_purchase_timestamp'].dt.year.max())
)

# Filter data berdasarkan rentang tahun
filtered_years_data = data[
    (data['order_purchase_timestamp'].dt.year >= start_year) & 
    (data['order_purchase_timestamp'].dt.year <= end_year)
]

# Pertanyaan 4: Jumlah total pesanan berdasarkan bulan
st.subheader("Jumlah Total Pesanan Berdasarkan Bulan")
monthly_orders = filtered_years_data.groupby(filtered_years_data['order_purchase_timestamp'].dt.to_period('M')).size().reset_index(name='total_orders')
monthly_orders['order_purchase_timestamp'] = monthly_orders['order_purchase_timestamp'].dt.to_timestamp()
st.line_chart(monthly_orders.set_index('order_purchase_timestamp')['total_orders'])
