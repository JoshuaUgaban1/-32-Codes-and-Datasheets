
import os
import argparse
import cv2
import numpy as np
import sys
import base64
import pyrebase
import time
import threading
from threading import Thread
import importlib.util
import serial
import json
import subprocess

subprocess.Popen(["python3", "/home/pi/tomato/tkinter_nav_menu.py"])

serial_data = serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0)
time.sleep(2)
serial_data.reset_input_buffer()
print("Arduino Serial Communication Started!")

config = {
  "apiKey": "AIzaSyCCFz7963ExMyf2vL6dtWsSu_ybXyDNDlA",
  "authDomain": "qppd-4bcba.firebaseapp.com",
  "databaseURL": "https://qppd-4bcba-default-rtdb.firebaseio.com/",
  "storageBucket": "qppd-4bcba.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

reset_data = {
    "turning": 0,
    "unripe": 0,
    "ripe": 0,
    "detection": "-"
    }
db.child("sorter").child("datas").update(reset_data)

reset_data = {
    "sorting": 0,
    "preservation": 0,
    }
db.child("sorter").child("operation").child("operate").update(reset_data)

def sendCommand(piCommand):
    try:
        print(piCommand)
        serial_data.write(piCommand.encode('utf-8'))
    except KeyboardInterrupt:
        print("Serial communication closed!")
        serial_data.close()
        
def getSerial():
    global arduino_response
    while True:
        if serial_data.in_waiting > 0:
            arduino_response = serial_data.readline().decode('utf-8').rstrip()
            print("RESPONSE:" + arduino_response)
            
            

def setSerial():
    global send_command, command
    send_command = False
    while True:
        if send_command:
            sendCommand(command)
            time.sleep(1)
            send_command = False

def getOperation():
    global previous_operation_state, previous_operation_state2, current_step, current_step2, send_command, command, arduino_response
    
    current_step = "STOP"
    current_step2 = "STOP"
    previous_operation_state = 0
    previous_operation_state2 = 0
    
    while True:
        datas = db.child("sorter").child("operation").child("operate").get()
        #print("DATA:" + str(datas))
        for data in datas.each():   
            if data.key() == "sorting":
                operate = data.val()
                
                if operate != previous_operation_state and operate == 1:
                    previous_operation_state = 1
                    current_step = "START"
                    print("Start operating sorter!")
                    print(current_step)
                    
                    command = "operate-dispenser:true"
                    send_command = True
                elif operate != previous_operation_state and operate == 0:
                    previous_operation_state = 0
                    current_step = "STOP"
                    print("Stop operating sorter!")
#                     sendCommand("operate-dispenser:false")
#                     time.sleep(1);
                    command = "stop-conveyor:true"
                    send_command = True
            elif data.key() == "preservation":
                operate2 = data.val()
                
                if operate2 != previous_operation_state2 and operate2 == 1:
                    previous_operation_state2 = 1
                    current_step2 = "PRESERVE"
                    print("Start operating preservation!")
                    print(current_step)
                    command = "operate-preservation:true"
                    send_command = True
                elif operate2 != previous_operation_state2 and operate2 == 0:
                    previous_operation_state2 = 0
                    current_step2 = "STOP"
                    print("Stop operating preservation!")
                    sendCommand("operate-preservation:false")
                    time.sleep(1);
                
                

# Define VideoStream class to handle streaming of video from webcam in separate processing thread
# Source - Adrian Rosebrock, PyImageSearch: https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True

# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--modeldir', help='Folder the .tflite file is located in',
                    required=True)
parser.add_argument('--graph', help='Name of the .tflite file, if different than detect.tflite',
                    default='detect.tflite')
parser.add_argument('--labels', help='Name of the labelmap file, if different than labelmap.txt',
                    default='labelmap.txt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.5)
parser.add_argument('--resolution', help='Desired webcam resolution in WxH. If the webcam does not support the resolution entered, errors may occur.',
                    default='1280x720')
parser.add_argument('--edgetpu', help='Use Coral Edge TPU Accelerator to speed up detection',
                    action='store_true')

args = parser.parse_args()

MODEL_NAME = args.modeldir
GRAPH_NAME = args.graph
LABELMAP_NAME = args.labels
min_conf_threshold = float(args.threshold)
resW, resH = args.resolution.split('x')
imW, imH = int(resW), int(resH)
use_TPU = args.edgetpu

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'       

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Check output layer name to determine if this model was created with TF2 or TF1,
# because outputs are ordered differently for TF2 and TF1 models
outname = output_details[0]['name']

if ('StatefulPartitionedCall' in outname): # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else: # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
videostream = VideoStream(resolution=(imW,imH),framerate=30).start()
time.sleep(1)

operate_thread = threading.Thread(target=getOperation)
operate_thread.daemon = True
operate_thread.start()

response_thread = threading.Thread(target=getSerial)
response_thread.daemon = True
response_thread.start()

command_thread = threading.Thread(target=setSerial)
command_thread.daemon = True
command_thread.start()
time.sleep(1)

scan_limit = 3
scan_counter = 1

isTomatoFirstTimeScanned = False

unripe_scan_count = 0
turning_scan_count =  0
ripe_scan_count = 0
pepper_scan_count = 0

unripe_count = 0
turning_count = 0
ripe_count = 0
pepper_count = 0

arduino_response = "-"
#current_step = "START"

#for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
while True:
    
    if current_step == "START":

        # Start timer (for calculating frame rate)
        t1 = cv2.getTickCount()

        # Grab frame from video stream
        frame1 = videostream.read()

        # Acquire frame and resize to expected shape [1xHxWx3]
        frame = frame1.copy()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects

        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
            
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 2)

                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2) # Draw label text
        
                if isTomatoFirstTimeScanned == True:
                    scan_counter = 0
                    isTomatoFirstTimeScanned = False
                    command =  "operate-dispenser:false"
                    send_command = True
                    time.sleep(1)
                
                if scan_counter == scan_limit:
                    scan_counter = 0
                    time.sleep(1)
                    
                    if pepper_scan_count > unripe_scan_count or pepper_scan_count > turning_scan_count or pepper_scan_count > ripe_scan_count:
                        command = "close-sorter:1"
                        send_command = True
                       
                    elif unripe_scan_count > turning_scan_count or unripe_scan_count > ripe_scan_count:
                        command = "operate-sorter-1:35"
                        send_command = True
                        
                        unripe_count += 1
                        unripe_to_save = {
                            "unripe": unripe_count,
                            "detection":"UNRIPE",
                            }
                        db.child("sorter").child("datas").update(unripe_to_save)
                        
                    elif turning_scan_count > unripe_scan_count or turning_scan_count > ripe_scan_count:
                        command = "operate-sorter-2:115"
                        send_command = True
                        
                        turning_count += 1
                        turning_to_save = {
                            "turning": turning_count,
                            "detection":"TURNING",
                            }
                        db.child("sorter").child("datas").update(turning_to_save)
                        
                    elif ripe_scan_count > unripe_scan_count or ripe_scan_count > turning_scan_count:
                        command = "operate-sorter-3:123"
                        send_command = True
                        
                        ripe_count += 1
                        ripe_to_save = {
                            "ripe": ripe_count,
                            "detection":"RIPE",
                            }
                        db.child("sorter").child("datas").update(ripe_to_save)
                
                    time.sleep(1)
                
                    command =  "operate-dispenser:true"
                    send_command = True
                    ripe_scan_count = 0
                    unripe_scan_count = 0
                    turning_scan_count= 0
                    pepper_scan_count = 0
            
                elif scan_counter > 0 and scan_counter < scan_limit:
                
                    scan_counter += 1
                
                    if object_name == "unripe":
                        unripe_scan_count += 1
                    elif object_name == "turning":
                        turning_scan_count += 1
                    elif object_name == "ripe":
                        ripe_scan_count += 1
                    elif object_name == "pepper":
                        pepper_scan_count += 1
                        
                    detection_to_save = {
                        "detection": object_name,
                        }
                    db.child("sorter").child("datas").update(detection_to_save)
                    
                elif scan_counter == 0:
                    
                    unripe_scan_count = 0
                    turning_scan_count = 0
                    ripe_scan_count = 0
                    command = "operate-dispenser:false"
                    send_command = True
                    
                    time.sleep(1)
                    scan_counter += 1
        
            else:
                if isTomatoFirstTimeScanned == False:
                    print("OPERATING HOPPER")
                    command = "operate-dispenser:true"
                    send_command  = True
                    isTomatoFirstTimeScanned = True
                    
                    print("Scan counter" + str(scan_counter))
                    if scan_counter == 5: 
                        scan_counter = 0
                    else:
                        scan_counter += 1

        # Draw framerate in corner of frame
        cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        #cv2.imshow('Object detector', frame)
    
        _, buffer = cv2.imencode('.jpg', frame)
        frame_as_bytes = buffer.tobytes()
        frame_as_base64 = base64.b64encode(frame_as_bytes).decode('utf-8')

        detection_data = {
        "detection": frame_as_base64,
        }
        json_data = json.dumps(detection_data)
    
        db.child("sorter").child("device").update(json.loads(json_data))

        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= 1/time1

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
    elif current_step2 == "PRESERVE":
        
        temperatures =  arduino_response.split(":")
        
        if temperatures[0] == "REF":
            print("SENDING TO APP")
            temperatures_to_save = {
                "temperature1": float(temperatures[1]),
                "temperature2": float(temperatures[2]),
                "temperature3": float(temperatures[3]),
                }
            db.child("sorter").child("temperatures").update(temperatures_to_save)
        time.sleep(1)
# Clean up
cv2.destroyAllWindows()
videostream.stop()
