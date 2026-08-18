import os, socket, time, argparse
parser = argparse.ArgumentParser(description="stream sender script")
fps = 1.0 / 30

parser.add_argument("--dir", type=str, default = r"/", help="Frames Directory")
parser.add_argument("--port", type = int, default = 5005, help= "port")
parser.add_argument("--ip", type=str, default="127.0.0.1", help="ip")
args = parser.parse_args()

imgs = os.listdir(args.dir)
imgs.sort()
s = socket.socket()
print("connecting")
connected = False
while not connected:
    try:
        s.connect((args.ip, args.port))
        connected = True
    except ConnectionRefusedError as e:
        print("Connection refused, retrying in 3s")
        time.sleep(3)

for name in imgs:
    t0=time.time()
    path = os.path.join(args.dir, name)
    with open(path, "rb") as f:
        data = f.read()
    s.sendall(f"{len(data):<16}".encode())
    s.sendall(data)
    t = time.time() - t0
    if t < fps:
        time.sleep(fps - t)
print("done")
s.close()
