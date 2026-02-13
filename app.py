import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd

st.set_page_config(page_title="Delivery Time Prediction", layout="wide")

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.hero {
    background: linear-gradient(90deg, #0f2027, #203a43, #2c5364);
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    color: white;
}
.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #2c5364;
    color: white;
    border-radius: 8px;
    padding: 10px 25px;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #203a43;
}
</style>
""", unsafe_allow_html=True)


def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":

        if choice == "Home":

            st.markdown("""
            <div class="hero">
            <h1>🚀 Delivery Time Prediction App</h1>
            <p>Machine Learning Powered by XGBoost</p>
            <p>Digital Skola Final Project</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
    
        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown("""
            <div class="card">
            <div class="section-title">📌 Tentang Aplikasi</div>
            Aplikasi ini memprediksi estimasi waktu pengantaran makanan berdasarkan berbagai faktor operasional seperti jumlah item, kategori restoran, jumlah kurir aktif, serta tingkat kesibukan kurir.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.image("assets/tukang_data.png", use_container_width=True)

        st.write("")

        st.markdown("""
        <div class="card">
        <div class="section-title">🤖 Model Machine Learning</div>
        Model menggunakan <b>XGBoost Regressor</b> dengan tahapan:
        <ul>
            <li>Handling Missing Values</li>
            <li>Exploratory Data Analysis</li>
            <li>One Hot Encoding</li>
            <li>Hyperparameter Tuning</li>
            <li>Model Evaluation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.info("👉 Silakan pilih menu 'Machine Learning App' di sidebar untuk melakukan prediksi.")
    


    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Delivery Time Prediction</h1>
                </div>
             """
    st.markdown(design, unsafe_allow_html=True)
    
    #structure form
    left, right = st.columns((2, 2))
    order_protocol = left.selectbox("Protocol", (1,2,3,4,5,6,7))
    store_primary_category_grouped = right.selectbox("Store Category", ('american', 'mexican', 'Uncategorized', 'indian', 'italian',
                                                                       'sandwich', 'thai', 'cafe', 'Other', 'pizza', 'chinese', 'burger',
                                                                       'breakfast', 'mediterranean', 'japanese', 'other', 'fast',
                                                                       'seafood', 'vietnamese', 'dessert'))
    total_items = left.number_input("Total item", min_value = 1)
    subtotal = right.number_input("Subtotal", min_value = 0)
    num_distinct_items = left.number_input("Jumlah jenis barang", min_value = 1)
    total_onshift_partners = right.number_input("Jumlah kurir", min_value = 1)
    total_busy_partners = left.number_input("Jumlah Kurir sedang mengantar", min_value = 1)
    total_outstanding_orders = right.number_input("Jumlah Kurir standby", min_value = 0)
    day_of_week_name = left.selectbox("Hari", options=["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"])
    min_item_price = right.number_input("Harga produk termurah", min_value = 0)
    max_item_price = left.number_input("Harga produk termahal", min_value = 0)
    hour = right.selectbox("Jam pesan", options=[1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    busy_ratio = total_busy_partners / total_onshift_partners
    load_ratio = total_outstanding_orders / total_onshift_partners
    idle_driver = total_onshift_partners - total_busy_partners
    avg_item_price = subtotal / total_items
    items_per_distinct = total_items / num_distinct_items
    button = st.button("Predict")
    #If button is clilcked
    if button:
        result = predict(order_protocol, total_items, subtotal, num_distinct_items, min_item_price, max_item_price, total_onshift_partners,
            total_busy_partners, total_outstanding_orders, hour, store_primary_category_grouped, busy_ratio, load_ratio,
            idle_driver, avg_item_price, items_per_distinct, day_of_week_name)
        st.success(f'makanan akan tiba dalam {result:.2f} menit')

def predict(order_protocol, total_items, subtotal, num_distinct_items, min_item_price, max_item_price, total_onshift_partners,
            total_busy_partners, total_outstanding_orders, hour, store_primary_category_grouped, busy_ratio, load_ratio,
            idle_driver, avg_item_price, items_per_distinct, day_of_week_name):
      
    #Preprocessing User Input
    input_data = pd.DataFrame({
        "order_protocol": [order_protocol],
        "total_items": [total_items],
        "subtotal": [subtotal],
        "num_distinct_items": [num_distinct_items],
        "min_item_price": [min_item_price],
        "max_item_price": [max_item_price],
        "total_onshift_partners": [total_onshift_partners],
        "total_busy_partners": [total_busy_partners],
        "total_outstanding_orders": [total_outstanding_orders],
        "hour": [hour],
        "store_primary_category_grouped": [store_primary_category_grouped],
        "busy_ratio": [busy_ratio],
        "load_ratio": [load_ratio],
        "idle_driver": [idle_driver],
        "avg_item_price": [avg_item_price],
        "items_per_distinct": [items_per_distinct],
        "day_of_week_name": [day_of_week_name]
    })

    #Making prediction
    prediction = XGB_Regression_Model.predict(input_data)
    
    return prediction[0]

if __name__ == "__main__":

    main()





















