import pyodbc
import flask
from flask_cors import CORS
import uuid
con_str = (
    "Driver={SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=DuLieu;"
    "Trusted_Connection=yes;"
)
conn = pyodbc.connect(con_str)
app = flask.Flask(__name__)
CORS(app)

#Chuyen doi tu SQL server sang danh sach json
def get_json_results(cursor):
    res = []
    keys = [i[0] for i in cursor.description] # lay ten cot cua cac bang
    for val in cursor.fetchall(): # lay du lieu cac bang
        res.append(dict(zip(keys, val)))
    return  res

#API tai khoan
@app.route('/auth/login', methods = ['POST'])
def login():
    try:
        user = flask.request.json.get("Username")
        pwd = flask.request.json.get("Password")

        cursor = conn.cursor()
        cursor.execute("select AccountID, Role, EmployeeID, CustomerID from Account where Username = ? and Password = ? AND IsActive = 1", (user, pwd))
        account = cursor.fetchone()

        if account:
            return flask.jsonify({
                "mess": "Login Successful",
                "AccountID": account[0],
                "Role": account[1]
            }), 200
        else:
            return flask.jsonify({"mess": "Wrong account of password"}), 401
    except Exception as e:
        return flask.jsonify({"mess": str(e)})

@app.route('/auth/register', methods = ['POST'])
def register():
    try:
        username = flask.request.json.get("Username")
        password = flask.request.json.get("Password")
        fullname = flask.request.json.get("Fullname")
        phone = flask.request.json.get("Phone")
        email = flask.request.json.get("Email")
        address = flask.request.json.get("Address")

        cursor = conn.cursor()
        cursor.execute("select AccountID from Account where Username = ?", (username,))
        if cursor.fetchone():
            return flask.jsonify({"mess": "Username already exists"}), 400
        cursor.execute("select CustomerID from Customer where Phone = ?", (phone,))
        if cursor.fetchone():
            return flask.jsonify({"mess": "Phone already exists"}), 400
        cursor.execute("select CustomerID from Customer where Email = ?", (email,))
        if cursor.fetchone():
            return flask.jsonify({"mess": "Email already exists"}), 400
        customer_id = "CUS_" + str(uuid.uuid4())[:6]
        account_id = "ACC_" + str(uuid.uuid4())[:6]

        sql_customer ="insert into customer(CustomerID, Fullname, Phone, Email, Address) values (?, ?, ?, ?, ?)"
        cursor.execute(sql_customer, (customer_id, fullname, phone, email, address))

        sql_account = "insert into account(AccountID, Username, Password, Role, IsActive, CustomerID) values (?,?,?, 'Customer', 1,?)"
        cursor.execute(sql_account, (account_id, username, password, customer_id))

        conn.commit()

        return flask.jsonify({
            "mess": "Register Successful",
            "Username": username
        }), 200
    except Exception as e:
        conn.rollback()
        print(e)
        return flask.jsonify({"mess": "Error system: " + str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)