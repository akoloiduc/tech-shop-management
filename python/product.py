from flask import Blueprint, request, jsonify
from .db import get_db_connection, rows_to_dict_list

bp = Blueprint('product', __name__)

@bp.route('/products', methods=['GET'])
def get_all_product():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all product!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/products/<ID>', methods=['GET'])
def get_product_by_id(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Product pr WHERE pr.ProductID = ?"
        cursor.execute(query, ID)
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify({"message":"Success!"}), 200
        else:
            return jsonify({"message":"Can't find this product!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/products', methods=['POST'])
def add_product():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        ProductID = data.get("ProductID")
        ProductName = data.get("ProductName")
        Brand = data.get("Brand") 
        CategoryID = data.get("CategoryID")
        Description = data.get("Description")
        Image = data.get("Image")
        Information = data.get("Information")
        Status = data.get("Status")
        query = """
                INSERT INTO Product(ProductID, ProductName, Brand, 
                Image, Description, Information, Status, CategoryID) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """
        cursor.execute(query, ProductID, ProductName, Brand, Image, Description, Information, Status, CategoryID)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/products/<ID>', methods=['PUT'])
def update_product(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        ProductName = data.get("ProductName")
        Brand = data.get("Brand") 
        CategoryID = data.get("CategoryID")
        Description = data.get("Description")
        Image = data.get("Image")
        Information = data.get("Information")
        Status = data.get("Status")
        query = """
                UPDATE Product SET ProductName = ?, Brand = ?,Image = ?,
                Description = ?, Information = ?, Status = ?, CategoryID = ?,
                WHERE ProductID = ?
                """
        cursor.execute(query, ProductName, Brand, Image, Description, Information, Status, CategoryID, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/products/<ID>', methods=['DELETE'])
def delete_product(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Product WHERE ProductID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()