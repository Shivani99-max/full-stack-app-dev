from flask import Blueprint, request, jsonify
from db import get_db_connection

borrow_bp = Blueprint("borrow_bp", __name__)

@borrow_bp.route("/borrow", methods=["POST"])
def request_equipment():
    data = request.get_json()
    user_id = data["user_id"]
    equipment_id = data["equipment_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # check availability
    cursor.execute("SELECT available_quantity FROM equipment WHERE id=%s", (equipment_id,))
    result = cursor.fetchone()
    if not result or result[0] <= 0:
        return jsonify({"error": "Not available"}), 400

    cursor.execute("""
        INSERT INTO borrow_requests (user_id, equipment_id, status)
        VALUES (%s, %s, 'Pending')
    """, (user_id, equipment_id))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"message": "Request submitted"}), 201
