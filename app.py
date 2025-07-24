from flask import Flask, render_template, request, redirect, url_for, flash
from math import radians, cos, sin, asin, sqrt
import requests

app = Flask(__name__)
app.secret_key = 'mighty_secret_key'  # Set a secret key for session management

# Example: Allowed location (latitude, longitude) and radius in meters
ALLOWED_LAT = 6.444853       # Lagos latitude example
ALLOWED_LON = 3.5167823       # Lagos longitude example
ALLOWED_RADIUS = 30000       # 200 meters

def haversine(lat1, lon1, lat2, lon2):
    # Calculate distance in meters between two lat/lon points
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

@app.route("/", methods=["GET", "POST"])
def attendance():
    if request.method == "POST":
        username = request.form.get("first_name")
        lat = float(request.form.get("latitude"))
        lon = float(request.form.get("longitude"))
        distance = haversine(lat, lon, ALLOWED_LAT, ALLOWED_LON)
        print(f"Distance calculated: {distance} meters")
        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "attendance_type": request.form.get("attendance_type"),
            "datetime": request.form.get("datetime"),
            "designation": request.form.get("designation"),
            "latitude": request.form.get("latitude"),
            "longitude": request.form.get("longitude"),
            "distance": distance,
        }
        
        if distance <= ALLOWED_RADIUS:
            n8n_webhook_url = "https://n8n.digitssphere.com/webhook/56328c97-aa19-4eea-bec2-0d54d5891b18"
            # Here you would typically send the data to n8n or another service
            try:
                response = requests.post(n8n_webhook_url, json=data)
                response.raise_for_status()
                print("Data sent successfully to n8n")
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to n8n: {e}")
                flash("Failed to send attendance data. Please try again.", "danger")
                return redirect(url_for('attendance'))
            flash(f"Attendance marked for {username}. Location validated!", "success")
        else:
            flash("You are not within the allowed location.", "danger")
        return redirect(url_for('attendance'))
    return render_template("attendance.html")
    
@app.route("/telegram_bot_campaign", methods=['GET', 'POST'])
def telegram():
    if request.method == "POST":
        pass 
    return render_template("telegram.html")

@app.route("/whatsapp_bot_campaign", methods=['GET', 'POST'])
def whatsapp():
    if request.method == "POST":
        pass 
    return render_template("whatsapp.html")





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099, debug=True)
    # app.run(debug=True)
