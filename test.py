import streamlit as st

with st.form("my_form"):
    st.header("Log in")
    user_type = st.selectbox("User Type", ["Select User Type", "Hospital", "Employee", "Donor"])
    user_name = st.text_input("User Id")
    btn = st.form_submit_button("Submit")

    if btn:
        st.write()