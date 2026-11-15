from flask import Flask, jsonify, request
import requests
import threading
import time

app = Flask(__name__)
# the jeepney route data
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
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

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
    data = request.get_json()

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