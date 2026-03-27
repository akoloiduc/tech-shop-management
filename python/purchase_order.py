from flask import Blueprint, request, jsonify
from .db import get_db_connection, rows_to_dict_list

bp = Blueprint('purchase_order', __name__)

@bp.route('/purchase_orders', methods=['GET'])
def get_all_purchase_order():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PurchaseOrder")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all purchase order!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_orders/<ID>')
def get_purchase_order_detail(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                SELECT * FROM PurchaseOrder po JOIN PurchaseOrderDetail pod 
                ON po.PurchaseOrderID = pod.PurchaseOrderID
                WHERE po.PurchaseOrderID = ?
                """
        cursor.execute(query, ID)
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't find this purchase order detail!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_orders', methods=['POST'])
def add_purchase_order():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        PurchaseOrderID = data.get("PurchaseOrderID")
        Status = data.get("Status")
        EmployeeID = data.get("EmployeeID")
        SupplierID = data.get("SupplierID") 
        query = """
                INSERT INTO PurchaseOrder(PurchaseOrderID, SupplierID, EmployeeID,  Status) 
                VALUES(?, ?, ?, ?)
                """
        cursor.execute(query, PurchaseOrderID, SupplierID, EmployeeID, Status)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_orders/<ID>', methods=['PUT'])
def update_purchase_order(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        Status = data.get("Status")
        EmployeeID = data.get("EmployeeID")
        SupplierID = data.get("SupplierID")
        query = """
                UPDATE PurchaseOrder SET SupplierID = ?, EmployeeID = ?, Status = ?
                WHERE PurchaseOrderID = ?
                """
        cursor.execute(query, SupplierID, EmployeeID, Status, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_orders/<ID>', methods=['DELETE'])
def delete_purchase_order(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM PurchaseOrder WHERE PurchaseOrderID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_orders/<ID>/confirm', methods=['POST'])
def confirm_purchase_order(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Status FROM PurchaseOrder WHERE PurchaseOrderID = ?", ID)
        status_list = rows_to_dict_list(cursor)
        if not status_list:
            return jsonify({"error": "Not found"}), 404
        if status_list[0]['Status'] == 'Pending Payment':
            return jsonify({"error": "This order has been confirmed before"}), 400
        cursor.execute("UPDATE PurchaseOrder SET Status = 'Pending Payment' WHERE PurchaseOrderID = ?", ID)   
        update_stock_query = """
            UPDATE pv
            SET pv.StockQuantity = pv.StockQuantity + pod.NumOrder
            FROM Productvariant pv
            JOIN PurchaseOrderDetail pod ON pv.ProductVariantID = pod.ProductVariantID
            WHERE pod.PurchaseOrderID = ?
            """
        cursor.execute(update_stock_query, ID)
        conn.commit()        
        return jsonify({"message": "Confirmed and stock updated successfully!"}), 200        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500    
    finally:
        if conn: 
            conn.close()

@bp.route('/purchase_orders/<ID>/pay', methods=['POST'])
def pay_purchase_order(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Status FROM PurchaseOrder WHERE PurchaseOrderID = ?", ID)
        status_list = rows_to_dict_list(cursor)
        
        if not status_list:
            return jsonify({"error": "Not found"}), 404
        if status_list[0]['Status'] == 'Completed':
            return jsonify({"error": "This order has been payed before"}), 400
        cursor.execute("UPDATE PurchaseOrder SET Status = 'Completed' WHERE PurchaseOrderID = ?", ID)
        conn.commit()        
        return jsonify({"message": "Confirmed and stock updated successfully!"}), 200        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500    
    finally:
        if conn: 
            conn.close()