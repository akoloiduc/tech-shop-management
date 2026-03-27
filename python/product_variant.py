from flask import Blueprint, request, jsonify
from db import get_db_connection, rows_to_dict_list

bp = Blueprint('variant', __name__)

@bp.route('/variants', methods=['GET'])
def get_all_variant():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Productvariant")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all product variant!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/variants/<ID>', methods=['GET'])
def get_variant_by_id(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Productvariant pv WHERE pv.ProductVariantID = ?"
        cursor.execute(query, ID)
        res = rows_to_dict_list(cursor)
        return jsonify(res), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/variants', methods=['POST'])
def add_variant():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        ProductVariantID = data.get("ProductVariantID")
        ProductID = data.get("ProductID")
        Capacity = data.get("Capacity") 
        Color = data.get("Color")
        StockQuantity = data.get("StockQuantity")
        SellingPrice = data.get("SellingPrice")
        query = """
                INSERT INTO Productvariant(ProductVariantID, ProductID, Color, Capacity,  
                SellingPrice, StockQuantity) 
                VALUES(?, ?, ?, ?, ?, ?)
                """
        cursor.execute(query, ProductVariantID, ProductID, Color, Capacity, SellingPrice, StockQuantity)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/variants/<ID>', methods=['PUT'])
def update_product(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        ProductID = data.get("ProductID")
        Capacity = data.get("Capacity") 
        Color = data.get("Color")
        StockQuantity = data.get("StockQuantity")
        SellingPrice = data.get("SellingPrice")
        query = """
                UPDATE Productvariant SET ProductID = ?, Color = ?, Capacity = ?,
                SellingPrice = ?, StockQuantity = ?
                WHERE ProductVariantID = ?
                """
        cursor.execute(query, ProductID, Color, Capacity, SellingPrice, StockQuantity, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/variants/<ID>', methods=['DELETE'])
def delete_variant(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Productvariant WHERE ProductVariantID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/products/<ID>/variants', methods=['GET'])
def get_product_variant(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                SELECT * FROM Productvariant pv 
                JOIN tblProduct pro ON pv.ProductID = pro.ProductID 
                WHERE pv.ProductID = ?
                """
        cursor.execute(query, ID)
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't find this product variant!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()