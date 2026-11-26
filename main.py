
from flask import Flask, jsonify, request

app = Flask(__name__)

# JEEPNEY ROUTE DATA
routes = [
    {
        "route_id": 1,
        "route_number": "12",
        "origin": "Public Market",
        "destination": "City Hall",
        "fare": 13
    },
    {
        "route_id": 2,
        "route_number": "15",
        "origin": "Dau Terminal",
        "destination": "Mabalacat",
        "fare": 15
    },
    {
        "route_id": 3,
        "route_number": "20",
        "origin": "Mabalacat",
        "destination": "Angeles City",
        "fare": 18
    }
]


# 1. GET ALL ROUTES
@app.route("/routes", methods=["GET"])
def get_routes():
    return jsonify(routes), 200


# 2. GET ONE ROUTE
@app.route("/routes/<int:id>", methods=["GET"])
def get_route(id):
    for route in routes:
        if route["route_id"] == id:
            return jsonify(route), 200

    return jsonify({"error": "Route not found"}), 404


# 3. ADD NEW ROUTE
@app.route("/routes", methods=["POST"])
def add_route():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    required_fields = ["route_number", "origin", "destination", "fare"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["fare"], (int, float)) or isinstance(data["fare"], bool) or data["fare"] < 0:
        return jsonify({"error": "Invalid fare"}), 400

    new_route = {
        "route_id": max([r["route_id"] for r in routes], default=0) + 1,
        "route_number": data["route_number"],
        "origin": data["origin"],
        "destination": data["destination"],
        "fare": data["fare"]
    }

    routes.append(new_route)

    return jsonify({
        "message": "Route added successfully",
        "route": new_route
    }), 201


# 4. UPDATE ROUTE
@app.route("/routes/<int:id>", methods=["PUT"])
def update_route(id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    required_fields = ["route_number", "origin", "destination", "fare"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not isinstance(data["fare"], (int, float)) or isinstance(data["fare"], bool) or data["fare"] < 0:
        return jsonify({"error": "Invalid fare"}), 400

    for route in routes:
        if route["route_id"] == id:
            route["route_number"] = data["route_number"]
            route["origin"] = data["origin"]
            route["destination"] = data["destination"]
            route["fare"] = data["fare"]

            return jsonify({
                "message": "Route updated successfully",
                "route": route
            }), 200

    return jsonify({"error": "Route not found"}), 404


# 5. DELETE ROUTE
@app.route("/routes/<int:id>", methods=["DELETE"])
def delete_route(id):
    for route in routes:
        if route["route_id"] == id:
            routes.remove(route)

            return jsonify({
                "message": "Route deleted successfully",
                "route_id": id
            }), 200

    return jsonify({"error": "Route not found"}), 404


# RUN THE APPLICATION
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
