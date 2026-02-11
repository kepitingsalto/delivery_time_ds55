import streamlit as st
import streamlit.components.v1 as stc
import pickle
import pandas as pd

with open('Model_XGB.pkl', 'rb') as file:
    XGB_Regression_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Delivery Time Prediction App</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Digital Skola Final Project</h4> 
                """

desc_temp = """ ### Loan Prediction App 
                This app is used by Credit team for deciding Loan Application
                
                #### Data Source
                Kaggle: Link <Masukkan Link>
                """

def main():
    stc.html(html_temp)
    menu = ["Home", "Machine Learning App"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown(desc_temp, unsafe_allow_html=True)
    elif choice == "Machine Learning App":
        run_ml_app()

def run_ml_app():
    design = """<div style="padding:15px;">
                    <h1 style="color:#fff">Loan Eligibility Prediction</h1>
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
    day_of_week_name = left.selectbox("Hari", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda x: {0: "Senin",  1: "Selasa", 2: "Rabu", 
                                                                                                    3:"Kamis", 4:"Jumat", 5:"Sabtu", 6:"Minggu"}[x])
    min_item_price = right.number_input("Harga produk termurah", min_value = 0)
    max_item_price = left.number_input("Harga produk termahal", min_value = 0)
    hour = right.number_input("Jam pesan", min_value = 0, max_value = 23, step = 1)
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
        st.success(f'makanan akan tiba dalam {result} menit')

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
    prediction = XGB_Regression_Model.predict([[order_protocol, total_items, subtotal, num_distinct_items, min_item_price, max_item_price, total_onshift_partners,
            total_busy_partners, total_outstanding_orders, hour, store_primary_category_grouped, busy_ratio, load_ratio,
            idle_driver, avg_item_price, items_per_distinct, day_of_week_name]])
    
    result = prediction
    return result

if __name__ == "__main__":

    main()






