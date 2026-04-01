import flask
import uuid
from db_config import conn, get_json_results

report_bp = flask.Blueprint('report_bp', __name__)

@report_bp.route('/revenue', methods=['GET'])
def report_revenue():
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(TotalPrice) FROM Bill WHERE IsDeleted = 0 and Status = 'Completed'")
    rev = cursor.fetchone()[0]
    if rev is None:
        rev = 0
    return flask.jsonify({"TotalRevenue": rev}), 200

@report_bp.route('/top-products', methods=['GET'])
def top_products():
    cursor = conn.cursor()
    sql = """
        SELECT TOP 10 
            pv.ProductID, pv.Color, pv.Capacity, SUM(bd.Num) as TotalSold
        FROM BillDetail bd
        INNER JOIN Bill b ON bd.BillID = b.BillID
        INNER JOIN ProductVariant pv ON bd.ProductVariantID = pv.ProductVariantID
        WHERE b.Status = 'Completed'
        GROUP BY pv.ProductID, pv.Color, pv.Capacity
        ORDER BY TotalSold DESC
    """
    cursor.execute(sql)
    return flask.jsonify(get_json_results(cursor)), 200