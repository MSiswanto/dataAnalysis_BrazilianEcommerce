import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(
    page_title="Dashboard E-commerce Brazil",
    page_icon="🛒",
    layout="wide"
)

# Custom styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #FAFAFA;
        color: #333;
    }
    h1, h2, h3 {
        font-weight: 600;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stSidebar {
        background-color: #ffffff;
        border-right: 1px solid #e6e6e6;
    }
    .stButton > button {
        background-color: #4B8BBE;
        color: white;
        border-radius: 8px;
    }
    .stButton > button:hover {
        background-color: #306998;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# Correct URL
customers_df = pd.read_csv("dashboard/customers_dataset.csv")
orders_df = pd.read_csv("dashboard/orders_dataset.csv")
order_items_df = pd.read_csv("dashboard/order_items_dataset.csv")
products_df = pd.read_csv("dashboard/products_dataset.csv")

#Tambahan 2025
# Sidebar


# Title
st.markdown("<h1 style='text-align: center;'>📈 E-commerce Brazil Dashboard</h1>", unsafe_allow_html=True)

# Simulated top/bottom customer revenue (replace with actual computation)
top_customer = {"monetary": 1890.00}
bottom_customer = {"monetary": 25.50}

col1, col2 = st.columns(2)
with col1:
    st.success(f"💰 **Top Customer Revenue**: ${top_customer['monetary']:.2f}")
with col2:
    st.warning(f"🔻 **Bottom Customer Revenue**: ${bottom_customer['monetary']:.2f}")

# Example chart
st.subheader("📊 Distribusi Monetary")
fig, ax = plt.subplots()
# sns.histplot(df['monetary'], kde=True, ax=ax)
ax.set_title("Distribusi Nilai Monetary Pelanggan")
ax.set_xlabel("Monetary Value")
ax.set_ylabel("Jumlah")
fig.subplots_adjust(bottom=0.25)
st.pyplot(fig)

# Tambahan visualisasi bisa ditaruh di bawah dengan struktur yang serupa


# --- Bagian 1: Jumlah Pelanggan Berdasarkan Kota dan State ---
st.title('Dashboard Data Pelanggan dan RFM Analysis')
st.header('Jumlah Pelanggan Berdasarkan Kota dan State')

# Menghitung jumlah pelanggan berdasarkan kota dan state
city_counts = customers_df['customer_city'].value_counts()
state_counts = customers_df['customer_state'].value_counts()

# Subplot dengan 2 Kolom
# Subplot dengan 2 bar chart menggunakan Streamlit Columns
col1, col2 = st.columns(2)

# Validasi data untuk city_counts dan state_counts
if city_counts.empty:
    st.warning("Data untuk jumlah pelanggan berdasarkan kota kosong.")
else:
    with col1:
        # Diagram Batang Kota
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=city_counts.head(10).index, y=city_counts.head(10).values, ax=ax, palette="crest")
        ax.set_title('Top 10 Kota', fontsize=14)
        ax.set_xlabel('Kota', fontsize=10)
        ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', labelsize=8)
        plt.tight_layout()
        st.pyplot(fig)

if state_counts.empty:
    st.warning("Data untuk jumlah pelanggan berdasarkan state kosong.")
else:
    with col2:
        # Diagram Batang State
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=state_counts.head(10).index, y=state_counts.head(10).values, ax=ax, palette="coolwarm")
        ax.set_title('Top 10 State', fontsize=14)
        ax.set_xlabel('State', fontsize=10)
        ax.set_ylabel('Jumlah Pelanggan', fontsize=10)
        ax.tick_params(axis='x', rotation=45)
        ax.tick_params(axis='y', labelsize=8)
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
#st.subheader('Tabel RFM')
#st.dataframe(rfm_df)

# Pelanggan dengan revenue terbesar dan terkecil
top_customer = rfm_df.loc[rfm_df['monetary'].idxmax()]
bottom_customer = rfm_df.loc[rfm_df['monetary'].idxmin()]

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

# Membuat DataFrame
df = pd.DataFrame(data)
df['month_year'] = pd.to_datetime(df['month_year'], format='%Y-%m')
df = df.sort_values('month_year')

with st.sidebar:
    st.markdown("""
        <div style="text-align: center;">
            <img src="https://images.unsplash.com/photo-1581090700227-1e8e939ef274?auto=format&fit=crop&w=600&q=80" 
                 style="max-width: 100%; border-radius: 10px;">
        </div>
    """, unsafe_allow_html=True)


# Sidebar untuk Dropdown
with st.sidebar:
    st.header('📅 Filter Data')
    selected_month = st.selectbox(
        "Select Month & Year:",
        ["Semua"] + df['month_year'].dt.strftime('%Y-%m').tolist()
    )

# Filter Data Berdasarkan Pilihan
filtered_df = df if selected_month == "Semua" else df[df['month_year'].dt.strftime('%Y-%m') == selected_month]

# Membuat Plot di Sidebar
fig, ax = plt.subplots(figsize=(5, 3))  # Ukuran kecil agar sesuai sidebar
sns.barplot(
    x=filtered_df['month_year'].dt.strftime('%Y-%m'), 
    y=filtered_df['count'], 
    palette="crest", 
    ax=ax
)

# Menambahkan Anotasi
for i, value in enumerate(filtered_df['count']):
    ax.text(i, value + max(filtered_df['count']) * 0.02, f"{value:,}", ha='center', fontsize=8)

# Menyesuaikan Label
ax.set_title("Jumlah Pesanan", fontsize=10)
ax.set_xlabel("", fontsize=8)
ax.set_ylabel("Pesanan", fontsize=8)
ax.tick_params(axis='x', rotation=45, labelsize=8)
ax.tick_params(axis='y', labelsize=8)

# Menampilkan Plot di Sidebar
st.sidebar.pyplot(fig)

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
