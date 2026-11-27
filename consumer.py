
import requests

BASE_URL = "http://127.0.0.1:5000/api/teams"

results = []

print("\n========== MINI TOURNAMENT API CONSUMER ==========")

try:
    # 1. GET ALL TEAMS
    response = requests.get(BASE_URL)

    results.append(("GET ALL TEAMS", response.status_code == 200))

    print("\nGET ALL TEAMS:", response.status_code)
    print(response.json())

    # 2. GET ONE TEAM
    response = requests.get(f"{BASE_URL}/1")

    results.append(("GET ONE TEAM", response.status_code == 200))

    print("\nGET ONE TEAM:", response.status_code)
    print(response.json())

    # 3. CREATE NEW TEAM
    new_team = {
        "team_name": "Yellow Tigers",
        "wins": 0,
        "losses": 0
    }

    response = requests.post(
        BASE_URL,
        json=new_team
    )

    results.append(("CREATE TEAM", response.status_code == 201))

    print("\nCREATE TEAM:", response.status_code)
    print(response.json())

    # 4. UPDATE TEAM
    if response.status_code == 201:
        team_id = response.json()["team_id"]

        updated_team = {
            "team_name": "Yellow Tigers",
            "wins": 2,
            "losses": 1
        }

        response = requests.put(
            f"{BASE_URL}/{team_id}",
            json=updated_team
        )

        results.append(("UPDATE TEAM", response.status_code == 200))

        print("\nUPDATE TEAM:", response.status_code)
        print(response.json())

        # 5. DELETE TEAM
        response = requests.delete(
            f"{BASE_URL}/{team_id}"
        )

        results.append(("DELETE TEAM", response.status_code == 200))

        print("\nDELETE TEAM:", response.status_code)
        print(response.json())

    # 6. ERROR TEST
    response = requests.get(f"{BASE_URL}/999")

    results.append(("ERROR TEST", response.status_code == 404))

    print("\nERROR TEST:", response.status_code)
    print(response.json())


except requests.exceptions.ConnectionError:
    print("\nERROR: Cannot connect to the partner API.")
    print("Make sure your partner's Flask API is running.")

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
