from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Temporary in-memory appointment storage
appointments = []

@app.route("/")
def home():
    return "AI Dental Assistant backend is running", 200

@app.route("/health")
def health():
    return jsonify(status="ok"), 200

@app.route("/check-availability", methods=["POST"])
def check_availability():
    data = request.get_json(force=True)

    date = data.get("date")
    time = data.get("time")
    doctor = data.get("doctor", "Any doctor")

    conflict = next(
        (appt for appt in appointments
         if appt["date"] == date and appt["time"] == time and appt["doctor"] == doctor),
        None
    )

    if conflict:
        return jsonify({
            "available": False,
            "message": f"Slot {date} at {time} with {doctor} is already booked."
        }), 200
    else:
        return jsonify({
            "available": True,
            "message": f"Slot {date} at {time} with {doctor} is free."
        }), 200

@app.route("/book-appointment", methods=["POST"])
def book_appointment():
    data = request.get_json(force=True)

    required_fields = ["name", "phone", "date", "time"]
    missing = [f for f in required_fields if f not in data or not data[f]]

    if missing:
        return jsonify({
            "success": False,
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    appointment = {
        "name": data["name"],
        "phone": data["phone"],
        "date": data["date"],
        "time": data["time"],
        "doctor": data.get("doctor", "Any doctor"),
        "reason": data.get("reason", "")
    }

    appointments.append(appointment)
    print("✅ New appointment:", appointment, flush=True)

    return jsonify({
        "success": True,
        "message": "Appointment saved.",
        "appointment": appointment
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
