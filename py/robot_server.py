from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
from Adafruit_I2C import Adafruit_I2C

i2c = Adafruit_I2C(0x68)
i2c.write8(0x6B,0)

def readS16Rev(i2c, reg):
    wrongOrder = i2c.readS16(reg)
    return i2c.reverseByteOrder(wrongOrder)

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        print self.path
        if (self.path == "/index.html" or self.path == "/"):
            f = open("html/index.html")
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(f.read())
            f.close
            return
        if (self.path == "/position"):
            
            
            accel_x = readS16Rev(i2c, 0x3B)
            accel_y = readS16Rev(i2c, 0x3D)
            accel_z = readS16Rev(i2c, 0x3F)
            
            print 'acc X:', accel_x
            print 'acc Y:', accel_y
            print 'acc Z:', accel_z
            
            
            gyro_x = readS16Rev(i2c, 0x43)
            gyro_y = readS16Rev(i2c, 0x45)
            gyro_z = readS16Rev(i2c, 0x47)
            
            print 'gyro X:', gyro_x
            print 'gyro Y:', gyro_y
            print 'gyro Z:', gyro_z

            
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'gyro': {'x':gyro_x,'y':gyro_y,'z':gyro_z}, 'acc':{'x':accel_x,'y':accel_y,'z':accel_z}}))
            return
        
def main():
    try:
        server = HTTPServer(('',5555), MyHandler)
        print 'starting server. curdir = ',curdir
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()
        
if __name__ == '__main__':
    main()
