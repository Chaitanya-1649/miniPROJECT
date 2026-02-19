from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import osmnx as ox
import networkx as nx
from geopy.geocoders import Nominatim
import random

app = Flask(__name__)
CORS(app)

geolocator = Nominatim(user_agent="route_app")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/find-route", methods=["POST"])
def find_route():
    try:
        data = request.json
        source_name = data["source"]
        dest_name = data["destination"]

        source_location = geolocator.geocode(source_name, timeout=10)
        dest_location = geolocator.geocode(dest_name, timeout=10)

        if not source_location or not dest_location:
            return jsonify({"error": "Location not found"}), 400

        source_coords = (source_location.latitude, source_location.longitude)
        dest_coords = (dest_location.latitude, dest_location.longitude)

        G = ox.graph_from_point(
            source_coords,
            dist=20000,
            network_type="drive"
        )

        orig_node = ox.distance.nearest_nodes(G, source_coords[1], source_coords[0])
        dest_node = ox.distance.nearest_nodes(G, dest_coords[1], dest_coords[0])

        route = nx.shortest_path(G, orig_node, dest_node, weight="length")

        route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
        route_length = nx.path_weight(G, route, weight="length")

        traffic = random.randint(10, 70)
        eta = round((route_length / 1000) / (40 - traffic*0.2) * 60, 2)

        return jsonify({
            "routes": [{
                "route": route_coords,
                "distance_km": round(route_length/1000,2),
                "traffic": traffic,
                "eta": eta
            }],
            "best_route": {
                "route": route_coords,
                "distance_km": round(route_length/1000,2),
                "traffic": traffic,
                "eta": eta
            }
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
