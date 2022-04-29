import streamlit as st
import utility as util
import configuration as config
import pandas

st.title("BLOOD MANAGEMENT DASHBOARD")



def login():
    with st.form("my_form"):
        st.header("Log in")
        user_type = st.selectbox("User Type", ["Select User Type", "Hospital", "Employee", "Donor"])
        user_name = st.text_input("User Id")
        user_pass = st.text_input("Password", type="password")
        login_submitted = st.form_submit_button("Login")
        if login_submitted:
            if user_type == "Hospital":
                result = util.get_query_result(config.CHECK_HOSPITAL_USER.format(user_name))
                st.write(result)
                if str(user_pass) == str(result[0][4]):
                    st.success("Successful")
                    is_already_logged_in = True
                    st.session_state["is_already_logged_in"] = is_already_logged_in
                    st.session_state["user_type"] = user_type
                    st.session_state["user_name"] = str(result[0][1])
                    st.session_state["user_id"] = str(result[0][0])
                    st.experimental_rerun()

                else:
                    st.error("Login failed")
                    login_submitted = False
            
            elif user_type == "Employee":
                result = util.get_query_result(config.CHECK_EMPLOYEE_USER.format(user_name))
                if str(user_pass) == str(result[0][6]):
                    st.success("Successful")
                    st.session_state["is_already_logged_in"] = True
                    st.session_state["user_type"] = user_type
                    st.session_state["user_name"] = str(result[0][1])
                    
                    st.session_state["user_blood_bank_id"] = str(result[0][7])
                    st.experimental_rerun()

                else:
                    st.error("Login failed")
                    login_submitted = False
                

            elif user_type == "Donor":
                result = util.get_query_result(config.CHECK_DONOR_USER.format(user_name))
                if str(user_pass) == str(result[0][6]):
                    st.success("Successful")
                    already_logged_in = True
                    st.session_state["is_already_logged_in"] = True
                    st.session_state["user_type"] = user_type
                    st.session_state["user_name"] = str(result[0][1])
                    st.session_state["user_id"] = str(result[0][0])
                    st.experimental_rerun()

                else:
                    st.error("Login failed")
                    login_submitted = False
                    
def add_donation():
    with st.form("add_donation_form",clear_on_submit=True):
        st.header("Add donation")
        donor_id = st.text_input("Donor id")
        bb_id = st.session_state["user_blood_bank_id"]
        b_id = st.text_input("Blood id")
        units = st.number_input("Units", 1, 20)
        add_donation_button = st.form_submit_button("Add")
        if add_donation_button:
            
            query = '''INSERT INTO bloodbank.donations(DONOR_ID, BLOOD_BANK_ID, BLOOD_ID, UNITS_DONATED)
            VALUES (%s, %s , %s, %s)'''
            data = (str(donor_id), int(bb_id), int(b_id), int(units))
            util.insert_data(query, data)
            st.write("Donation Added Successfully")

def check_blood_stock():
    with st.form("check_blood_stock",clear_on_submit=True):

        blood_group = st.selectbox("Blood Group", ["A", "B", "AB", "O"])
        rh_factor = st.selectbox("RH Factor", ["positive", "negative"])
        search_stock = st.form_submit_button("Search")
        if search_stock:
            result = util.get_sql_result_df(config.CHECK_STOCK_LEVEL.format(blood_group, rh_factor))
            st.table(result)


################# HOSPITAL FUNCTION ####################

def create_order():
    with st.form("create_order_form", clear_on_submit=True):
        st.header("Create Order")
        hospital_id = st.text_input("Hospital Id")
        bb_id = st.text_input("Blood Bank Id")
        b_id = st.text_input("Blood Id")
        quantity = st.number_input("Quantity", 1, 20)
        create_order_button = st.form_submit_button("Create")
        if create_order_button:
            
            query = '''INSERT INTO bloodbank.orders(HOSPITAL_ID,BLOOD_BANK_ID,BLOOD_ID,QUANTITY,ORDER_DATE,STATUS)
            VALUES (%s, %s , %s, %s, %s)'''
            data = (str(hospital_id), int(bb_id), int(b_id), int(quantity), "PENDING")
            util.insert_data(query, data)
            st.write("Order has been created Successfully")

def track_order():
    with st.form("track_order", clear_on_submit=True):

        o_id = st.text_input("Order Id")
        check_order_id = st.form_submit_button("Check")
        if check_order_id:
            result = util.get_sql_result_df(config.CHECK_ORDER_STATUS.format(o_id))
            st.table(result)


####################### DONOR SECTION ########################
def view_last_donation():
    
    result = util.get_sql_result_df(config.VIEW_LAST_DONATIONS.format(st.session_state["user_id"]))
    st.table(result)

def show_notification():
    result = util.get_query_result(config.SHOW_NOTIFICATION.format(st.session_state["user_id"]))
    # st.write(result)
    return True if result[0][0] > 1 else False

def view_event():
    
    result = util.get_sql_result_df(config.VIEW_EVENT.format(st.session_state["user_id"]))
    st.table(result)


if __name__ == '__main__':
    if 'is_already_logged_in' in st.session_state:
       is_already_logged_in = True
    else:
        login()

    
    if st.session_state.get("user_type") == "Employee":
        with st.sidebar:
            st.write(f"Welcome {st.session_state['user_name']}")
            #emploee_log_out = st.button("Log out")
            add_donations = st.button("Add donations")
            blood_stock_button = st.button("Check blood stock")

        if add_donations or st.session_state.get("add_donations_action"):
            st.session_state["add_donations_action"] = True
            # st.session_state["blood_stock_button_action"]=False
            add_donation()

        if blood_stock_button or st.session_state.get("blood_stock_button_action"):
            st.session_state["blood_stock_button_action"] = True
            # st.session_state["add_donations_action"] = False
            check_blood_stock()

    if st.session_state.get("user_type") == "Hospital":
        with st.sidebar:
            st.write(f"Welcome {st.session_state['user_name']}")
            #emploee_log_out = st.button("Log out")
            create_order_btn = st.button("Create Order")
            track_order_btn = st.button("Track Order")

        if create_order_btn or st.session_state.get("create_order_action"):
            st.session_state["create_order_action"] = True
            # st.session_state["blood_stock_button_action"]=False
            create_order()

        if track_order_btn or st.session_state.get("track_order_action"):
            st.session_state["track_order_action"] = True
            # st.session_state["add_donations_action"] = False
            track_order()

    if st.session_state.get("user_type") == "Donor":
        with st.sidebar:
            st.write(f"Welcome {st.session_state['user_name']}")
            #emploee_log_out = st.button("Log out")
            view_last_donations = st.button("View last 5 donations")
            view_events = st.button("View Events")
            # temp = show_notification()
            # st.write(temp)
            # update_donor_details =  st.button("Update donor details")
            if show_notification():
                st.write("Low Blood Stock! Please Donate")
                
            

        if view_last_donations:
            # st.session_state["create_order_action"] = True
            # st.session_state["blood_stock_button_action"]=False
            view_last_donation()

        if view_events:
            # st.session_state["create_order_action"] = True
            # st.session_state["blood_stock_button_action"]=False
            view_event()

        # if track_order_btn or st.session_state.get("track_order_action"):
        #     st.session_state["track_order_action"] = True
        #     # st.session_state["add_donations_action"] = False
        #     track_order()



