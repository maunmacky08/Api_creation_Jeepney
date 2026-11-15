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
