import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data (update file paths sesuai lokasi Anda)

customers_df = pd.read_csv('https://raw.githubusercontent.com/MSiswanto/dataAnalysis_BrazilianEcommerce/main/dashboard/customers_dataset.csv')
orders_df = pd.read_csv('https://raw.githubusercontent.com/MSiswanto/dataAnalysis_BrazilianEcommerce/main/dashboard/orders_dataset.csv')
order_items_df = pd.read_csv('https://raw.githubusercontent.com/MSiswanto/dataAnalysis_BrazilianEcommerce/dashboard/main/order_items_dataset.csv')
products_df = pd.read_csv('https://raw.githubusercontent.com/MSiswanto/dataAnalysis_BrazilianEcommerce/main/dashboard/products_dataset.csv')

# --- Bagian 1: Jumlah Pelanggan Berdasarkan Kota dan State ---
st.title('Dashboard Data Pelanggan dan RFM Analysis')
st.header('Jumlah Pelanggan Berdasarkan Kota dan State')

# Menghitung jumlah pelanggan berdasarkan kota dan state
city_counts = customers_df['customer_city'].value_counts()
state_counts = customers_df['customer_state'].value_counts()

# Subplot dengan 2 bar chart
fig, ax = plt.subplots(1, 2, figsize=(15, 6))

# Diagram Batang Kota
sns.barplot(x=city_counts.head(10).index, y=city_counts.head(10).values, ax=ax[0])
ax[0].set_title('Top 10 Kota dengan Pelanggan Terbanyak')
ax[0].set_xlabel('Kota')
ax[0].set_ylabel('Jumlah Pelanggan')
ax[0].tick_params(axis='x', rotation=45)

# Diagram Batang State
sns.barplot(x=state_counts.head(10).index, y=state_counts.head(10).values, ax=ax[1])
ax[1].set_title('Top 10 State dengan Pelanggan Terbanyak')
ax[1].set_xlabel('State')
ax[1].set_ylabel('Jumlah Pelanggan')
ax[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

# --- Bagian 2: RFM Analysis ---
st.header('RFM Analysis')

# Tambahkan kolom 'total_price' ke order_items_df
order_items_df['total_price'] = order_items_df['price'] * order_items_df['freight_value']

# Gabungkan data orders dan order_items
merged_df = pd.merge(order_items_df, orders_df, on='order_id', how='inner')

# Menghitung Recency
snapshot_date = pd.Timestamp('2018-09-30')  # Tentukan snapshot date
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])
recency = (snapshot_date - merged_df.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days

# Menghitung Frequency
frequency = merged_df.groupby('customer_id')['order_id'].nunique()

# Menghitung Monetary
monetary = merged_df.groupby('customer_id')['total_price'].sum()

# Membuat DataFrame RFM
rfm_df = pd.DataFrame({
    'recency': recency,
    'frequency': frequency,
    'monetary': monetary
}).reset_index()

# Menampilkan tabel RFM
st.subheader('Tabel RFM')
st.dataframe(rfm_df)

# Pelanggan dengan revenue terbesar dan terkecil
top_customer = rfm_df.loc[rfm_df['monetary'].idxmax()]
bottom_customer = rfm_df.loc[rfm_df['monetary'].idxmin()]

# Menampilkan informasi tambahan
st.subheader('Informasi Pelanggan')
st.write(f"Pelanggan dengan revenue terbesar: {top_customer.to_dict()}")
st.write(f"Pelanggan dengan revenue terkecil: {bottom_customer.to_dict()}")

# Visualisasi RFM Metrics
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

sns.histplot(rfm_df['recency'], kde=False, bins=20, ax=ax[0], color='blue')
ax[0].set_title('Distribusi Recency')

sns.histplot(rfm_df['frequency'], kde=False, bins=20, ax=ax[1], color='green')
ax[1].set_title('Distribusi Frequency')

sns.histplot(rfm_df['monetary'], kde=False, bins=20, ax=ax[2], color='red')
ax[2].set_title('Distribusi Monetary')

plt.tight_layout()
st.pyplot(fig)

# --- Bagian 3: Visualisasi Tambahan ---
st.header('Visualisasi Tambahan')

# Pesanan per Bulan
st.subheader('Jumlah Pesanan per Bulan')

# Data month_year
data = {
    "month_year": [
        "2016-09", "2016-10", "2016-12", "2017-01", "2017-02", "2017-03", "2017-04",
        "2017-05", "2017-06", "2017-07", "2017-08", "2017-09", "2017-10", "2017-11",
        "2017-12", "2018-01", "2018-02", "2018-03", "2018-04", "2018-05", "2018-06",
        "2018-07", "2018-08", "2018-09"
    ],
    "count": [
        4, 318, 1, 797, 1766, 2680, 2400, 3691, 3241, 4021, 4325, 4281, 4626, 7535,
        5666, 7268, 6724, 7208, 6939, 6872, 6167, 6291, 6459, 1
    ]
}

df = pd.DataFrame(data)
df['month_year'] = pd.to_datetime(df['month_year'], format='%Y-%m')
df = df.sort_values('month_year')

fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(x=df['month_year'].dt.strftime('%Y-%m'), y=df['count'], palette="crest", ax=ax)

# Menambahkan anotasi pada setiap batang
for i, value in enumerate(df['count']):
    ax.text(i, value + max(df['count']) * 0.02, f"{value:,}", ha='center', fontsize=8)

# Menambahkan judul dan label
ax.set_title("Jumlah Pesanan per Bulan", fontsize=16)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Jumlah Pesanan", fontsize=12)
ax.tick_params(axis='x', rotation=45, labelsize=10)

# Menampilkan plot
plt.tight_layout()
st.pyplot(fig)

# --- Plot for Top and Bottom Products ---
st.subheader('Top 10 Produk Paling Laku dan Tidak Laku')

# Gabungkan data produk dan transaksi berdasarkan product_id
merged_df = pd.merge(order_items_df, products_df, on='product_id', how='inner')

# Hitung jumlah penjualan untuk setiap produk
product_sales = merged_df.groupby(['product_id', 'product_category_name']).size().reset_index(name='sales_count')

# Cari produk paling laku dan tidak laku
top_products = product_sales.sort_values('sales_count', ascending=False).head(10)  # Top 10 paling laku
bottom_products = product_sales.sort_values('sales_count', ascending=True).head(10)  # Top 10 tidak laku

# Visualisasi
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Subplot 1: Produk Paling Laku
sns.barplot(x=top_products['sales_count'], y=top_products['product_category_name'], palette="crest", ax=ax[0])
ax[0].set_title("Top 10 Produk Paling Laku", fontsize=16)
ax[0].set_xlabel("Jumlah Penjualan", fontsize=12)
ax[0].set_ylabel("Kategori Produk", fontsize=12)

# Subplot 2: Produk Tidak Laku
sns.barplot(x=bottom_products['sales_count'], y=bottom_products['product_category_name'], palette="coolwarm", ax=ax[1])
ax[1].set_title("Top 10 Produk Paling Tidak Laku", fontsize=16)
ax[1].set_xlabel("Jumlah Penjualan", fontsize=12)
ax[1].set_ylabel("Kategori Produk", fontsize=12)

# Menampilkan plot
plt.tight_layout()
st.pyplot(fig)
