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


# CONSUMER / TESTING SCRIPT
def consumer():

    time.sleep(2)

    results = []

    print("\nJEEPNEY ROUTE FINDER TEST")

    # GET ALL
    response = requests.get("http://127.0.0.1:5000/routes")
    results.append(("GET /routes", response.status_code == 200))
    print("\nGET ALL ROUTES:", response.status_code)
    print(response.json())

    # GET ONE
    response = requests.get("http://127.0.0.1:5000/routes/1")
    results.append(("GET /routes/1", response.status_code == 200))
    print("\nGET ONE ROUTE:", response.status_code)
    print(response.json())

    # ADD ROUTE
    new_route = {
        "route_number": "25",
        "origin": "Mabalacat",
        "destination": "Dau",
        "fare": 15
    }

    response = requests.post(
        "http://127.0.0.1:5000/routes",
        json=new_route
    )
    return jsonify({"error": "Route not found"}), 404
    results.append(("POST /routes", response.status_code == 201))
    print("\nADD ROUTE:", response.status_code)
    print(response.json())

    # UPDATE ROUTE
    if response.status_code == 201:
        route_id = response.json()["route"]["route_id"]

        updated_route = {
            "route_number": "25",
            "origin": "Mabalacat",
            "destination": "Angeles City",
            "fare": 18
        }

        response = requests.put(
            f"http://127.0.0.1:5000/routes/{route_id}",
            json=updated_route
        )

        results.append(("PUT /routes", response.status_code == 200))
        print("\nUPDATE ROUTE:", response.status_code)
        print(response.json())

        # DELETE ROUTE
        response = requests.delete(
            f"http://127.0.0.1:5000/routes/{route_id}"
        )

        results.append(("DELETE /routes", response.status_code == 200))
        print("\nDELETE ROUTE:", response.status_code)
        print(response.json())

    # ERROR TEST
    response = requests.get("http://127.0.0.1:5000/routes/999")

    results.append(("GET /routes/999", response.status_code == 404))
    print("\nERROR TEST:", response.status_code)
    print(response.json())

    # SUMMARY REPORT
    print("\n========== SUMMARY REPORT ==========")

    for name, result in results:
        if result:
            print(name, "- PASSED")
        else:
            print(name, "- FAILED")

    passed = sum(result for name, result in results)

    print("\nTotal Tests:", len(results))
    print("Passed:", passed)
    print("Failed:", len(results) - passed)
    print("====================================")


# RUN THE APPLICATION
if _name_ == "_main_":

    threading.Thread(target=consumer, daemon=True).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
