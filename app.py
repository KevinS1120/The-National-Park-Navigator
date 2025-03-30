from flask import Flask, render_template, jsonify, request
import urllib.request
import json

app = Flask(__name__)

# NPS API key
API_KEY = 'eAfhBkc9dGOTbkvmAnSBwSggJSnevWJfKsxyrh98'

# List of all US National Parks with their codes
NATIONAL_PARKS = [
    {"name": "Acadia", "code": "ACAD"},
    {"name": "American Samoa", "code": "NPSA"}, 
    {"name": "Arches", "code": "ARCH"},
    {"name": "Badlands", "code": "BADL"},
    {"name": "Big Bend", "code": "BIBE"},
    {"name": "Biscayne", "code": "BISC"},
    {"name": "Black Canyon of the Gunnison", "code": "BLCA"},
    {"name": "Bryce Canyon", "code": "BRCA"},
    {"name": "Buffalo National River", "code": "BUFF"},
    {"name": "Canyonlands", "code": "CANY"},
    {"name": "Capitol Reef", "code": "CARE"},
    {"name": "Carlsbad Caverns", "code": "CAVE"},
    {"name": "Channel Islands", "code": "CHIS"},
    {"name": "Congaree", "code": "CONG"},
    {"name": "Crater Lake", "code": "CRLA"},
    {"name": "Cuyahoga Valley", "code": "CUVA"},
    {"name": "Death Valley", "code": "DEVA"},
    {"name": "Denali", "code": "DENA"},
    {"name": "Dry Tortugas", "code": "DRTO"},
    {"name": "Everglades", "code": "EVER"},
    {"name": "Gates of the Arctic", "code": "GAAR"},
    {"name": "Gateway Arch", "code": "JEFF"},
    {"name": "Glacier", "code": "GLAC"},
    {"name": "Glacier Bay", "code": "GLBA"},
    {"name": "Grand Canyon", "code": "GRCA"},
    {"name": "Grand Teton", "code": "GRTE"},
    {"name": "Great Basin", "code": "GRBA"},
    {"name": "Great Sand Dunes", "code": "GRSA"},
    {"name": "Great Smoky Mountains", "code": "GRSM"},
    {"name": "Guadalupe Mountains", "code": "GUMO"},
    {"name": "Haleakalā", "code": "HALE"},
    {"name": "Hawai'i Volcanoes", "code": "HAVO"},
    {"name": "Hot Springs", "code": "HOSP"},
    {"name": "Indiana Dunes", "code": "INDU"},
    {"name": "Isle Royale", "code": "ISRO"},
    {"name": "Joshua Tree", "code": "JOTR"},
    {"name": "Katmai", "code": "KATM"},
    {"name": "Kenai Fjords", "code": "KEFJ"},
    {"name": "Kings Canyon", "code": "KICA"},
    {"name": "Kobuk Valley", "code": "KOVA"},
    {"name": "Lake Clark", "code": "LACL"},
    {"name": "Lassen Volcanic", "code": "LAVO"},
    {"name": "Mammoth Cave", "code": "MACA"},
    {"name": "Mesa Verde", "code": "MEVE"},
    {"name": "Mount Rainier", "code": "MORA"},
    {"name": "New River Gorge", "code": "NERI"},
    {"name": "North Cascades", "code": "NOCA"},
    {"name": "Olympic", "code": "OLYM"},
    {"name": "Petrified Forest", "code": "PEFO"},
    {"name": "Pinnacles", "code": "PINN"},
    {"name": "Redwood", "code": "REDW"},
    {"name": "Rocky Mountain", "code": "ROMO"},
    {"name": "Saguaro", "code": "SAGU"},
    {"name": "Sequoia", "code": "SEKI"},
    {"name": "Shenandoah", "code": "SHEN"},
    {"name": "Theodore Roosevelt", "code": "THRO"},
    {"name": "Virgin Islands", "code": "VIIS"},
    {"name": "Voyageurs", "code": "VOYA"},
    {"name": "White Sands", "code": "WHSA"},
    {"name": "Wind Cave", "code": "WICA"},
    {"name": "Wrangell-St. Elias", "code": "WRST"},
    {"name": "Yellowstone", "code": "YELL"},
    {"name": "Yosemite", "code": "YOSE"},
    {"name": "Zion", "code": "ZION"}
]

@app.route('/')
def index():
    return render_template('index.html', parks=NATIONAL_PARKS)

@app.route('/get_image', methods=['POST'])
def get_image():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))

        if not data.get("data"):
            return jsonify({"error": "No image found"})
        
        park_data = data["data"][0]
        images = park_data.get("images", [])

        if not images:
            return jsonify({"error": "No images available"})
        
        image = images[0]
        return jsonify({
            "url": image.get("url"),
            "title": image.get("title"),
            "caption": image.get("caption")
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_park_fees', methods=['POST'])
def get_fees():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))
        
        if not data.get("data"):
            return jsonify({"entrance_fees": [], "entrance_passes": []})
            
        park_data = data["data"][0]
        
        return jsonify({
            "entrance_fees": park_data.get("entranceFees", []),
            "entrance_passes": park_data.get("entrancePasses", [])
        })
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code}"})
    except urllib.error.URLError as e:
        return jsonify({"error": f"URL Error: {e.reason}"})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON response"})
    
@app.route('/get_alerts', methods=['POST'])
def get_alerts():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/alerts?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))

        alerts = []
        for alert in data.get("data", []):
            alert_info = {
                "title": alert.get("title", "No title"),
                "description": alert.get("description", "No description available."),
                "category": alert.get("category", "No category specified"),
                "url": alert.get("url", "")
            }
            alerts.append(alert_info)

        return jsonify({"alerts": alerts})
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code}"})
    except urllib.error.URLError as e:
        return jsonify({"error": f"URL Error: {e.reason}"})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON response"})

@app.route('/get_campgrounds', methods=['POST'])
def get_campgrounds():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/campgrounds?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))
        
        campgrounds = []
        for campground in data["data"]:
            camp_info = {
                "name": campground["name"],
                "description": campground.get("description", "No description available."),
                "totalSites": campground.get("totalSites", 0),
                "reservationUrl": campground.get("reservationUrl", "https://www.recreation.gov/")
            }
            campgrounds.append(camp_info)
            
        return jsonify({"campgrounds": campgrounds})
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code}"})
    except urllib.error.URLError as e:
        return jsonify({"error": f"URL Error: {e.reason}"})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON response"})
    
@app.route('/get_activities', methods=['POST'])
def get_activities():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/parks?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))

        if not data.get("data"):
            return jsonify({"activities": []})

        activities = []
        park_data = data["data"][0]
        
        for activity in park_data.get("activities", []):
            activities_info = {
                "name": activity["name"],
            }
            activities.append(activities_info)
        
        return jsonify({"activities": activities})
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code}"})
    except urllib.error.URLError as e:
        return jsonify({"error": f"URL Error: {e.reason}"})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON response"})
    
@app.route('/get_amenities', methods=['POST'])
def get_amenities():
    park_code = request.json.get('park_code')
    url = f"https://developer.nps.gov/api/v1/amenities?parkCode={park_code}&api_key={API_KEY}"

    try:
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req).read()
        data = json.loads(response.decode('utf-8'))
        
        amenities = []
        for amenity in data["data"]:
            amenities_info = {
                "name": amenity["name"],
            }
            amenities.append(amenities_info)
            
        return jsonify({"amenities": amenities})
    except urllib.error.HTTPError as e:
        return jsonify({"error": f"HTTP Error: {e.code}"})
    except urllib.error.URLError as e:
        return jsonify({"error": f"URL Error: {e.reason}"})
    except json.JSONDecodeError: 
        return jsonify({"error": "Error decoding JSON response"})
    
if __name__ == '__main__':
    app.run(debug=True)