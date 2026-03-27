from flask import Blueprint, request, jsonify
from .db import get_db_connection, rows_to_dict_list

bp = Blueprint('category', __name__)

@bp.route('/categories', methods=['GET'])
def get_all_category():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Category")
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't get all category!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/categories/<ID>', methods=['GET'])
def get_category_by_id(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM Category ct WHERE ct.CategoryID = ?"
        cursor.execute(query, ID)
        res = rows_to_dict_list(cursor)
        if res:
            return jsonify(res), 200
        else:
            return jsonify({"message":"Can't find this category!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/categories', methods=['POST'])
def add_categories():
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        CategoryID = data.get("CategoryID")
        Name = data.get("Name")
        query = "INSERT INTO Category(CategoryID, Name) VALUES(?, ?)"
        cursor.execute(query, CategoryID, Name)
        conn.commit()
        return jsonify({"message":"Success!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/categories/<ID>', methods=['PUT'])
def update_category(ID):
    conn = None
    try:
        data = request.get_json()
        conn = get_db_connection()
        cursor = conn.cursor()
        Name = data.get("Name")
        query = "UPDATE Category SET Name = ? WHERE CategoryID = ?"
        cursor.execute(query, Name, ID)
        conn.commit()
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()

@bp.route('/categories/<ID>', methods=['DELETE'])
def delete_category(ID):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM Category WHERE CategoryID = ?"
        cursor.execute(query, ID)
        conn.commit()   
        return jsonify({"message":"Success!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500     
    finally:
        if conn: conn.close()