from os import curdir, sep

# This is a hack to patch slow socket.getfqdn calls that
# BaseHTTPServer (and its subclasses) make.
# See: http://bugs.python.org/issue6085
# See: http://www.answermysearches.com/xmlrpc-server-slow-in-python-how-to-fix/2140/

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def _bare_address_string(self):
    host, port = self.client_address[:2]
    return '%s' % host

BaseHTTPRequestHandler.address_string = \
        _bare_address_string

# End hack.

import json
from time import time
from Adafruit_I2C import Adafruit_I2C

i2c = Adafruit_I2C(0x68)
i2c.write8(0x6B,0)

compass = Adafruit_I2C(0x1e)
compass.write8(0x00,0x70)
compass.write8(0x01,0xA0)
compass.write8(0x02,0)

def readS16Rev(i2c, reg):
    wrongOrder = i2c.readS16(reg)
    unsigned = i2c.reverseByteOrder(wrongOrder)
    signed = unsigned
    if (signed>0x7fff):
        signed = signed - 0xffff
    return signed
    
def readS12Rev(i2c, reg):
    highByte = i2c.readS8(reg)
    lowByte = i2c.readS8(reg+1)
    unsigned = highByte * 256 + lowByte
    signed = unsigned
    if (signed>0x7ff):
        signed = signed - 0xfff
    return signed

class MyHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        startTime = time()
        print self.path,startTime,"ms"
        if (self.path == "/index.html" or self.path == "/"):
            f = open("html/index.html")
            
            data = f.read()
            f.close
            prepareTime = time()
            print 'time to read data from file:',prepareTime-startTime
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            writeTime = time()
            print 'time to headers data to output :',writeTime-prepareTime
            self.wfile.write(data)
            
            
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

            output_json = json.dumps({'gyro': {'x':gyro_x,'y':gyro_y,'z':gyro_z}, 'acc':{'x':accel_x,'y':accel_y,'z':accel_z}})

            prepareTime = time()
            print 'time to read data from accel:',prepareTime-startTime
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()
            writeTime = time()
            print 'time to headers data to output :',writeTime-prepareTime
            self.wfile.write(output_json)
            print 'time to write data to output :',time()-writeTime
            
        if (self.path == "/compass"):            
            
            status = compass.readS8(0x09)
            print 'compass status:',status
            
            compass_x = readS12Rev(compass, 0x03)
            compass_y = readS12Rev(compass, 0x07)
            compass_z = readS12Rev(compass, 0x05)
            
            print 'compass X:', compass_x
            print 'compass Y:', compass_y
            print 'compass Z:', compass_z
            
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'compass': {'x':compass_x,'y':compass_y,'z':compass_z}}))
            
        if (self.path == "/compass/selftest"):            
            
        
            status = compass.readS8(0x09)
            print 'compass status:',status
            
            compass_x = readS16Rev(compass, 0x03)
            compass_y = readS16Rev(compass, 0x07)
            compass_z = readS16Rev(compass, 0x05)
            
            print 'compass X:', compass_x
            print 'compass Y:', compass_y
            print 'compass Z:', compass_z
            
            self.send_response(200)
            self.send_header('Content-type','text/json')
            self.end_headers()
            self.wfile.write(json.dumps({'compass': {'x':compass_x,'y':compass_y,'z':compass_z}}))
            
        endTime = time()
        print 'time to response:',endTime-startTime
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
