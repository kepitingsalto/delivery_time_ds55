import streamlit as st
import streamlit.components.v1 as stc
import pickle

with open('xgb_regression_model.pkl', 'rb') as file:
    XGB_Regression_Model = pickle.load(file)

html_temp = """<div style="background-color:#000;padding:10px;border-radius:10px">
                <h1 style="color:#fff;text-align:center">Loan Eligibility Prediction App</h1> 
                <h4 style="color:#fff;text-align:center">Made for: Credit Team</h4> 
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
                </div
             """
    st.markdown(design, unsafe_allow_html=True)
    
    #structure form
    left, right = st.columns((2, 2))
    order_protocol = left.selectbox("Protocol", (1,2,3,4,5,6,7))
    store_primary_category = right.selectbox("Store Category", ('american', 'mexican', 'Uncategorized', 'indian', 'italian',
       'sandwich', 'thai', 'cafe', 'Other', 'pizza', 'chinese', 'burger',
       'breakfast', 'mediterranean', 'japanese', 'other', 'fast',
       'seafood', 'vietnamese', 'dessert'))
    total_items = left.number_input("Total item", min_value = 0)
    subtotal = right.number_input("Subtotal", min_value = 0)
    num_distinct_items = left.number_input("Jumlah jenis barang", min_value = 0)
    total_onshift_partners = right.number_input("Jumlah kurir", min_value = 0)
    total_busy_partners = left.number_input("Jumlah Kurir sedang mengantar", min_value = 0)
    total_outstanding_orders = right.number_input("Jumlah Kurir standby", min_value = 0)
    button = st.button("Predict")
    #If button is clilcked
    if button:
        result = predict(order_protocol, store_primary_category, total_items, subtotal, num_distinct_items, total_onshift_partners
                         ,total_busy_partners, total_outstanding_orders)
        st.success(f'makanan akan tiba dalam {result} menit')

def predict(order_protocol, store_primary_category, total_items, subtotal, num_distinct_items, total_onshift_partners
                         ,total_busy_partners, total_outstanding_orders):
    
    #Preprocessing User Input

    #Making prediction
    prediction = XGB_Regression_Model.predict([[order_protocol, store_primary_category, total_items, subtotal, num_distinct_items, total_onshift_partners
                         ,total_busy_partners, total_outstanding_orders]])
    
    result = prediction
    return result

if __name__ == "__main__":

    main()


