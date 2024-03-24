from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import time
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)

model = YOLO('yolov8n.pt')
names = model.names

frame = None
bw = False  # Black and white mode
model1 = False  # Model 1 toggle
model2 = False  # Model 2 toggle
fr = False  # Frame rate toggle
sharp = False  # Sharpness toggle
pause = False  # Pause toggle
one = False
original = None

def apply_operations(frame):
    global bw, model1, model2, fr, sharp, pause, one, original

    if bw:
        new_frame = frame.copy()
        new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
        return new_frame

    elif model1:
        if not one:
            new_frame = frame.copy()
            prediction = model.predict(new_frame)
            for result in prediction:
                for boxes in result.boxes:
                    if(float(boxes.conf[0])>0.6):
                        boxes = boxes.to('cpu')
                        xyxy = boxes.xyxy.tolist()[0]
                        conf = float(boxes.conf[0])*100
                        clss = int(boxes.cls[0])
                        tl = xyxy[:2]
                        br = xyxy[2:]
                        new_frame = cv2.rectangle(new_frame,(int(tl[0]),int(tl[1])),(int(br[0]),int(br[1])),(0,255,0),2)
                        new_frame = cv2.putText(new_frame,str(names[clss])+" "+'{:.2f}'.format(conf)+"%",(int(tl[0]-20),int(tl[1]-20)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
            return new_frame

    elif model2:
        new_frame = frame.copy()
        new_frame = cv2.cvtColor(new_frame, cv2.COLOR_BGR2RGB)
        return new_frame
    
    elif sharp:
        new_frame = frame.copy()
        kernel = np.array([[-1, -1, -1],
                    [-1, 9, -1],
                    [-1, -1, -1]])
        new_frame = cv2.filter2D(new_frame, -1, kernel)
        return new_frame
    
    elif pause:
        imgray = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        new_frame = frame.copy()
        cv2.drawContours(new_frame, contours, -1, (0,255,0), 3)
        return new_frame
    
    elif fr:
        new_frame = frame.copy()
        blue, green, red = cv2.split(new_frame)
        red = cv2.add(red, 50)
        new_frame = cv2.merge([blue, green, red])
        return new_frame
    
    return frame

def generate_frames():
    while True:
        global frame
        if frame is not None:
            frame_processed = apply_operations(frame)
            ret, buffer = cv2.imencode('.jpg', frame_processed)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.2)

@app.route('/image')
def image():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/bw', methods=['POST'])
def toggle_bw():
    global bw
    bw = not bw
    return jsonify({'toggle_variable': 'Black and white:' + str(bw)})

@app.route('/model1', methods=['POST'])
def toggle_model1():
    global model1
    model1 = not model1
    if not model1:
        one = True
    return jsonify({'toggle_variable': 'YOLO detector:'+str(model1)})

@app.route('/model2', methods=['POST'])
def toggle_model2():
    global model2
    model2 = not model2
    return jsonify({'toggle_variable': 'BGR to RGB:'+str(model2)})

@app.route('/fr', methods=['POST'])
def toggle_fr():
    global fr
    fr = not fr
    return jsonify({'toggle_variable': 'Red intense:'+str(fr)})

@app.route('/sharp', methods=['POST'])
def toggle_sharp():
    global sharp
    sharp = not sharp
    return jsonify({'toggle_variable': 'Sharpness:'+str(sharp)})

@app.route('/pause', methods=['POST'])
def toggle_pause():
    global pause
    pause = not pause
    return jsonify({'toggle_variable': 'Contours'+str(pause)})

@app.route('/upload', methods=['POST'])
def upload_file():
    global frame,original
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    frame = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    original = frame.copy()
    return jsonify({'filename': file.filename})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
