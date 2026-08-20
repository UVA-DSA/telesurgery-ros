import argparse
import socket
import numpy as np
import cv2
import random
import os

parser = argparse.ArgumentParser(description="stream receiver script")
parser.add_argument("--port", type= int, default= 5005, help="port to connect to")
parser.add_argument("--blur_amount", type=int, default=35, help="how blurry the image will be with the blurred glitch (1 - 99)")
parser.add_argument("--glitch_blur", action= "store_true", help="blurred image glitch")

parser.add_argument("--glitch_black", action ="store_true", help="random black frame glitch")
parser.add_argument("--black_prob", type=float, default=0.05, help="probability of a black frame (0.0 to 1.0)")

parser.add_argument("--save_dir", type=str, default=None, help="directory folder where the video will be saved")
parser.add_argument("--output_name", type=str, default="recorded_stream.mp4", help="name of the saved video file")
args = parser.parse_args() #gets variables from user

if args.blur_amount % 2 == 0: # makes sure the blur is odd
    args.blur_amount = max(1, args.blur_amount - 1) 

output_path = None
if args.save_dir:
    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)
    output_path = os.path.join(args.save_dir, args.output_name)

s = socket.socket()
s.bind(("0.0.0.0", args.port))
s.listen(1)
print("waiting")
conn, addr = s.accept()
print("connected:", addr)

buf = b""
cv2.namedWindow("stream", cv2.WINDOW_NORMAL) #creates the window
video_writer = None

while True:
    while len(buf) < 16:
        d = conn.recv(4096) #makes sure waits to get full item
        if not d:
            break
        buf += d
    if len(buf) < 16:
        break
        
    size = int(buf[:16]) #grabs just the size off the whole item
    buf = buf[16:]
    
    while len(buf) < size:
        d = conn.recv(4096)
        if not d:
            break
        buf += d
    if len(buf) < size: #exits if the whole thing was not grabbed
        break
        
    img = buf[:size]
    buf = buf[size:]
    
    frame = cv2.imdecode(np.frombuffer(img, np.uint8), 1)
    if frame is not None:
        height, width, _ = frame.shape
        
        if args.glitch_black and random.random() < args.black_prob:
            frame = np.zeros_like(frame) # makes the frame black with a random chance
        else:
            if args.glitch_blur:
                frame = cv2.GaussianBlur(frame, (args.blur_amount, args.blur_amount), 0) # blurs the simulators frame
                
        cv2.imshow("stream", frame) #shows the frame
        
        if output_path:
            if video_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(output_path, fourcc, 30, (width, height)) #saving the video
            video_writer.write(frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'): #cuts of the stream early if q is pressed
            break

if video_writer is not None:
    video_writer.release()
conn.close()
s.close()
cv2.destroyAllWindows()
