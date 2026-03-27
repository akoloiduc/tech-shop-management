from flask import Blueprint, request, jsonify
from .db import get_db_connection, rows_to_dict_list

bp = Blueprint('purchase_order_detail', __name__)

@bp.route('/purchase_order_details', methods=['GET'])
def get_all_purchase_order_detail():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PurchaseOrderDetail")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all purchase order detail!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_order_details', methods=['POST'])
def add_purchase_order_detail():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        PurchaseOrderID = data.get("PurchaseOrderID")
        PurchaseOrderDetailID = data.get("PurchaseOrderDetailID") 
        NumOrder = data.get("NumOrder")
        ProductVariantID = data.get("ProductVariantID")
        ImportPrice = data.get("ImportPrice")
        query = """
                INSERT INTO PurchaseOrderDetail(PurchaseOrdeerDetailID, PurchaseOrderID, 
                ProductVariantID, NumOrder, ImportPrice) VALUES(?, ?, ?, ?, ?)
                """
        cursor.execute(query, PurchaseOrderDetailID, PurchaseOrderID, ProductVariantID, NumOrder, ImportPrice)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_order_details/<ID>', methods=['PUT'])
def update_purchase_order_detail(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        PurchaseOrderID = data.get("PurchaseOrderID") 
        NumOrder = data.get("NumOrder")
        ProductVariantID = data.get("ProductVariantID")
        ImportPrice = data.get("ImportPrice")
        query = """
                UPDATE PurchaseOrderDetail SET PurchaseOrderID = ?, ProductVariantID = ?, NumOrder = ?,
                ImportPrice = ? WHERE PurchaseOrderDetailID = ?
                """
        cursor.execute(query, PurchaseOrderID, ProductVariantID, NumOrder, ImportPrice, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/purchase_order_detail/<ID>', methods=['DELETE'])
def delete_purchase_order_detail(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM PurchaseOrderDetail WHERE PurchaseOrderID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()