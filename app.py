import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd

with open('Model_XGB.pkl', 'rb') as file:
    XGB_Regression_Model = pickle.load(file)

html_temp = """
<div style="
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.2);
">
    <h1 style="
        color: white;
        font-size: 42px;
        margin-bottom: 10px;
        font-weight: 700;
        letter-spacing: 1px;
    ">
        🚚 Delivery Time Prediction App
    </h1>

    <p style="
        color: #f0f0f0;
        font-size: 20px;
        margin-bottom: 25px;
    ">
        Powered by XGBoost Machine Learning Model
    </p>

    <div style="
        background-color: rgba(255,255,255,0.1);
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    ">
        <p style="
            color: white;
            font-size: 16px;
            line-height: 1.6;
        ">
            This application predicts delivery duration based on 
            historical data and advanced machine learning modeling.
            <br><br>
            Enter your delivery parameters and get instant predictions 
            with high accuracy.
        </p>
    </div>
</div>
"""
st.markdown(html_temp, unsafe_allow_html=True)


desc_temp = """


Aplikasi ini digunakan untuk memprediksi estimasi waktu pengantaran makanan berdasarkan berbagai faktor operasional seperti jumlah item, kategori restoran, jumlah kurir aktif, serta tingkat kesibukan kurir.

Model yang digunakan dalam aplikasi ini adalah **XGBoost Regressor** yang telah melalui proses:

- Handling Missing Values
- Exploratory Data Analysis
- Feature Engineering  
- Handling Categorical Variables (One Hot Encoding)  
- Hyperparameter Tuning  
- Model Evaluation  

---

### Fitur yang Digunakan dalam Model

Beberapa variabel yang memengaruhi estimasi waktu pengantaran antara lain:

- Order Protocol  
- Store Primary Category  
- Total Items & Subtotal  
- Jumlah Jenis Barang  
- Harga Produk (Min & Max)  
- Jumlah Kurir Aktif & Sibuk  
- Rasio Kesibukan Kurir (Busy Ratio)  
- Rasio Beban Order (Load Ratio)  
- Jam Pemesanan  
- Hari Pemesanan  

Model ini dirancang untuk membantu meningkatkan efisiensi operasional serta memberikan estimasi waktu pengantaran yang lebih akurat kepada pelanggan.

---

Silakan pilih menu **Machine Learning App** untuk melakukan prediksi.
"""

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.image("assets/tukang_data.png", use_container_width=True)
        st.markdown(desc_temp, unsafe_allow_html=True)
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























