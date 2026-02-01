from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np

app = Flask(__name__, static_folder='static', template_folder='templates')

camera = cv2.VideoCapture(0)

skin_tone = "Not detected"
skin_type = "Not detected"
brand = "Not available"
recommendation = "Not available"

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def generate_frames():
    global skin_tone, recommendation, brand, skin_type

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)
            v_mean = np.mean(hsv[:, :, 2])

            if v_mean > 180:
                skin_tone = "Fair"
                recommendation = "SPF 50+ | PA++++"
                brand = "Neutrogena Ultra Sheer SPF50 / La Roche-Posay Anthelios"
                skin_type = "Oily"
            elif v_mean > 120:
                skin_tone = "Medium"
                recommendation = "SPF 30+ | PA+++"
                brand = "Nivea Sun Protect SPF30 / Lotus Herbals Safe Sun SPF30"
                skin_type = "Normal"
            else:
                skin_tone = "Dark"
                recommendation = "SPF 30 | PA++"
                brand = "Garnier Ambre Solaire SPF30 / Biotique Sun Protect SPF30"
                skin_type = "Dry"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/result')
def result():
    return jsonify({
        "skin_tone": skin_tone,
        "recommendation": recommendation,
        "brand": brand,
        "skin_type": skin_type
    })


@app.route('/dispense')
def dispense():
    return jsonify({"status": "Dispensing sunscreen..."})


if __name__ == "__main__":
    app.run(debug=True)
