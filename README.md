# Geolocation Attendance App

A simple web application for location-restricted employee attendance, built with Flask. The app ensures that attendance can only be marked when the user is within a specified geographic area.

## Features
- **Location Validation:** Uses browser geolocation to ensure users are within the allowed radius before submitting attendance.
- **Attendance Form:** Collects first name, last name, attendance type (Check In, Check Out, Break), date & time, and designation.
- **Live Location Fetch:** Users must allow geolocation and click "Get My Location" to enable attendance submission.
- **Data Submission:** Attendance data is sent to an external webhook (n8n) if the user is within the allowed area.
- **User Feedback:** Success and error messages are displayed for user actions.

## Technologies Used
- Python 3
- Flask
- HTML5, CSS3, JavaScript (for geolocation)
- [requests](https://docs.python-requests.org/en/latest/) (for webhook integration)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd geolaction-attendance-app
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install Flask requests
   ```

## Usage
1. **Run the app:**
   ```bash
   python app.py
   ```
2. **Open your browser and go to:**
   [http://localhost:8099](http://localhost:8099)
3. **Mark attendance:**
   - Fill in the form fields.
   - Click "Get My Location" and allow location access.
   - Submit your attendance if you are within the allowed area.

## Configuration
- **Allowed Location:**
  - The allowed latitude, longitude, and radius are set in `app.py`:
    ```python
    ALLOWED_LAT = 6.444853  # Example: Lagos latitude
    ALLOWED_LON = 3.5167823  # Example: Lagos longitude
    ALLOWED_RADIUS = 30000  # in meters (default: 30,000m)
    ```
- **Webhook URL:**
  - The attendance data is sent to an n8n webhook. Update the `n8n_webhook_url` in `app.py` as needed.

## Project Structure
```
├── app.py                # Main Flask application
├── templates/
│   └── attendance.html   # Attendance form template
├── static/
│   └── logo.jpeg         # (Optional) Logo for branding
```

## License
This project is provided for educational and demonstration purposes. Please adapt and secure it for production use. 