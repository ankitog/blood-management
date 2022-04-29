HOST= "wilp-db-bloodbank.cqcpwlsqyqz8.us-east-1.rds.amazonaws.com"
USER= "admin"
PASSWORD= "wilpProjPass"
PORT=3306
DATABASE="bloodbank"

CHECK_HOSPITAL_USER = "SELECT * FROM hospital where NAME= '{}'"
CHECK_EMPLOYEE_USER = "SELECT * FROM employee where NAME= '{}'"
CHECK_DONOR_USER = "SELECT * FROM donor where NAME= '{}'"

CHECK_STOCK_LEVEL = '''select b.BLOOD_GROUP,b.RH_FACTOR,b.COST, bs.QUANTITY from bloodbank.BloodStock bs ,  bloodbank.blood b where 
b.BLOOD_GROUP = '{}' AND b.RH_FACTOR = '{}'
AND b.ID=bs.BLOOD_ID
AND bs.QUANTITY>0'''

CHECK_ORDER_STATUS = "SELECT ORDER_ID, STATUS FROM bloodbank.orders WHERE ORDER_ID= {}"

VIEW_LAST_DONATIONS = '''select * from bloodbank.donations where DONOR_ID = '{}' order by DONATION_DATE desc limit 5;'''

SHOW_NOTIFICATION = '''SELECT 
    count(bs.ID)
FROM
    bloodbank.donorRegistration dr,
    bloodbank.BloodStock bs,
    bloodbank.donor d
WHERE
    1 = 1
        AND dr.BLOOD_BANK_ID = bs.BLOOD_BANK_ID
        AND dr.DONOR_ID = '{}'
        and dr.DONOR_ID=d.DONOR_ID
        AND d.BLOOD_ID = bs.BLOOD_ID
        AND bs.QUANTITY <= 35;'''


VIEW_EVENT = '''SELECT  e.*  FROM  bloodbank.event e,  bloodbank.donorRegistration dr  WHERE  dr.BLOOD_BANK_ID = e.BLOOD_BANK_ID  AND dr.DONOR_ID = '{}'  and e.EVENT_DATE >sysdate()'''