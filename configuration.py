HOST= "wilp-db-bloodbank.cqcpwlsqyqz8.us-east-1.rds.amazonaws.com"
USER= "admin"
PASSWORD= "wilpProjPass"
PORT=3306
DATABASE="bloodbank"

CHECK_HOSPITAL_USER = "SELECT * FROM hospital where NAME= '{}'"
CHECK_EMPLOYEE_USER = "SELECT * FROM employee where NAME= '{}'"
CHECK_DONOR_USER = "SELECT * FROM donor where NAME= '{}'"

CHECK_STOCK_LEVEL = '''SELECT ID FROM bloodbank.BloodStock WHERE BLOOD_ID = 
(SELECT ID FROM bloodbank.blood WHERE BLOOD_GROUP = '{}' AND RH_FACTOR = '{}') AND QUANTITY > 0'''

CHECK_ORDER_STATUS = "SELECT STATUS FROM bloodbank.orders WHERE ORDER_ID={}"