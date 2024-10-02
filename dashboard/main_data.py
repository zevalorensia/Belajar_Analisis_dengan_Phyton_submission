import pandas as pd

# Mengatur path file CSV dengan relative path
orders_df = pd.read_csv('../data/orders_dataset.csv')
order_items_df = pd.read_csv('../data/order_items_dataset.csv')
products_df = pd.read_csv('../data/products_dataset.csv')
order_reviews_df = pd.read_csv('../data/order_reviews_dataset.csv')
order_payments_df = pd.read_csv('../data/order_payments_dataset.csv')

# Menggabungkan data seperti yang sebelumnya dijelaskan
merged_data = orders_df.merge(order_items_df, on='order_id').merge(products_df, on='product_id')
merged_reviews = merged_data.merge(order_reviews_df, on='order_id')
final_data = merged_reviews.merge(order_payments_df, on='order_id')

# Menyimpan hasil penggabungan ke CSV
final_data.to_csv('../data/main_data.csv', index=False)

print("Data berhasil digabungkan dan disimpan sebagai 'data/main_data.csv'")
