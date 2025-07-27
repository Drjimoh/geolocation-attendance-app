from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from math import radians, cos, sin, asin, sqrt
import requests
import os

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

@app.route("/", methods=["GET"])
def landing():
    return render_template("landing.html")

@app.route("/leads", methods=["GET"])
def leads_landing():
    return render_template("leads_landing.html")

@app.route("/leads/process", methods=["POST"])
def process_leads():
    try:
        # Get form data
        business_category = request.form.get("business_category")
        location = request.form.get("location")
        number_of_leads = request.form.get("number_of_leads")
        email = request.form.get("email")
        service_type = request.form.get("service_type")
        
        # Get PayPal payment details
        paypal_order_id = request.form.get("paypal_order_id")
        paypal_payer_id = request.form.get("paypal_payer_id")
        paypal_email = request.form.get("paypal_email")
        paypal_name = request.form.get("paypal_name")
        
        # Calculate price based on service type and number of leads
        base_price = 50  # Base price for scrape only
        if service_type == "scrape_ai":
            base_price = 100
        elif service_type == "full_outreach":
            base_price = 200
        
        # Add cost per lead
        price_per_lead = 2
        total_price = base_price + (int(number_of_leads) * price_per_lead)
        
        # If PayPal payment details are present, send to n8n webhook
        if paypal_order_id and paypal_payer_id:
            n8n_webhook_url = "https://n8n.yourdomain.com/webhook/scrape-start"
            data = {
                "business_category": business_category,
                "location": location,
                "number_of_leads": number_of_leads,
                "email": email,
                "service_type": service_type,
                "total_price": total_price,
                "paypal_order_id": paypal_order_id,
                "paypal_payer_id": paypal_payer_id,
                "paypal_email": paypal_email,
                "paypal_name": paypal_name
            }
            
            try:
                response = requests.post(n8n_webhook_url, json=data)
                response.raise_for_status()
                print(f"Data sent to n8n webhook: {response.json()}")
                return jsonify({"success": True, "message": "Order processed successfully"})
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to n8n: {e}")
                return jsonify({"success": False, "message": "Payment successful but order processing failed. Please contact support."}), 500
        else:
            return jsonify({"success": False, "message": "Payment verification failed. Please try again."}), 400
            
    except Exception as e:
        print(f"Error processing leads order: {e}")
        return jsonify({"success": False, "message": "An error occurred. Please try again."}), 500

@app.route("/leads/success")
def leads_success():
    return render_template("leads_success.html")

@app.route("/attendance", methods=["GET", "POST"])
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
    
@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name")
    email = request.form.get("email")
    company = request.form.get("company")
    message = request.form.get("message")
    n8n_webhook_url = "https://n8n.digitssphere.com/webhook/dc75eff5-cdb7-4a5f-b0b8-9bd35a070b64"
    data = {
        "name": name,
        "email": email,
        "company": company,
        "message": message
    }
    try:
        response = requests.post(n8n_webhook_url, json=data)
        print(response.json())
        response.raise_for_status()
        contact_message = {"success": True, "text": "Thank you for contacting me! I will get back to you soon."}
    except requests.exceptions.RequestException as e:
        contact_message = {"success": False, "text": "Failed to send your message. Please try again later."}
    return render_template("landing.html", contact_message=contact_message)

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
