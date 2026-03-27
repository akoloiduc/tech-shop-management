from flask import Blueprint, request, jsonify
from db import get_db_connection, rows_to_dict_list

bp = Blueprint('supplier', __name__)

@bp.route('/suppliers', methods=['GET'])
def get_all_supplier():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Supplier")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all supplier!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/suppliers', methods=['POST'])
def add_supplier():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        SupplierID = data.get("SupplierID")
        SupplierName = data.get("SupplierName")
        Address = data.get("Address") 
        Phone = data.get("Phone")
        Email = data.get("Email")
        query = "INSERT INTO Supplier(SupplierID, SupplierName, Address, Phone, Email) VALUES(?, ?, ?, ?, ?)"
        cursor.execute(query, SupplierID, SupplierName, Address, Phone, Email)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/suppliers/<ID>', methods=['PUT'])
def update_supplier(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        SupplierName = data.get("SupplierName")
        Address = data.get("Address") 
        Phone = data.get("Phone")
        Email = data.get("Email")
        query = "UPDATE Supplier SET, SupplierName = ?, Address = ?, Phone = ?, Email = ?, WHERE SupplierID = ?"
        cursor.execute(query, SupplierName, Address, Phone, Email, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/suppliers/<ID>', methods=['DELETE'])
def delete_supplier(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Supplier WHERE SupplierID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()