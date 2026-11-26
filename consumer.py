
import requests

BASE_URL = "http://127.0.0.1:5000"

results = []

print("\n========== JEEPNEY ROUTE FINDER CONSUMER ==========")


# 1. GET ALL ROUTES
try:
    response = requests.get(f"{BASE_URL}/routes")
    results.append(("GET ALL ROUTES", response.status_code == 200))

    print("\nGET ALL ROUTES:", response.status_code)
    print(response.json())

    # 2. GET ONE ROUTE
    response = requests.get(f"{BASE_URL}/routes/1")
    results.append(("GET ONE ROUTE", response.status_code == 200))

    print("\nGET ONE ROUTE:", response.status_code)
    print(response.json())

    # 3. ADD NEW ROUTE
    new_route = {
        "route_number": "25",
        "origin": "Mabalacat",
        "destination": "Dau",
        "fare": 15
    }

    response = requests.post(
        f"{BASE_URL}/routes",
        json=new_route
    )

    results.append(("ADD ROUTE", response.status_code == 201))

    print("\nADD ROUTE:", response.status_code)
    print(response.json())

    # 4. UPDATE ROUTE
    if response.status_code == 201:
        route_id = response.json()["route"]["route_id"]

        updated_route = {
            "route_number": "25",
            "origin": "Mabalacat",
            "destination": "Angeles City",
            "fare": 18
        }

        response = requests.put(
            f"{BASE_URL}/routes/{route_id}",
            json=updated_route
        )

        results.append(("UPDATE ROUTE", response.status_code == 200))

        print("\nUPDATE ROUTE:", response.status_code)
        print(response.json())

        # 5. DELETE ROUTE
        response = requests.delete(
            f"{BASE_URL}/routes/{route_id}"
        )

        results.append(("DELETE ROUTE", response.status_code == 200))

        print("\nDELETE ROUTE:", response.status_code)
        print(response.json())

    # ERROR TEST
    response = requests.get(f"{BASE_URL}/routes/999")

    results.append(("ERROR TEST", response.status_code == 404))

    print("\nERROR TEST:", response.status_code)
    print(response.json())


except requests.exceptions.ConnectionError:
    print("\nERROR: Cannot connect to the API.")
    print("Make sure main.py is running first.")

except requests.exceptions.RequestException as error:
    print("\nREQUEST ERROR:", error)


# SUMMARY REPORT
print("\n========== SUMMARY REPORT ==========")

for name, passed in results:
    if passed:
        print(name, "- PASSED")
    else:
        print(name, "- FAILED")

total_passed = sum(passed for name, passed in results)

print("\nTotal Tests:", len(results))
print("Passed:", total_passed)
print("Failed:", len(results) - total_passed)

print("====================================")
