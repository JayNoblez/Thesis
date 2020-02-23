from network import LoRa
from machine import RTC
import uos
import pycom
import socket
import ubinascii
import ustruct
import crypto
import utime
import array

off = 0x000000
# Dictionary for values. Can be easily expanded
value_dict = {"humidity": "", "temperature": "", "ambient_light": "", "pressure": ""}

# function to define random values in this scenario to be sent as uplink over LoRa.
def random():
   r = crypto.getrandbits(32)
   return ((r[0]<<24)+(r[1]<<16)+(r[2]<<8)+r[3])/4294967295.0

#setting the indicator on the pycom device
pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # set LED to red
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868) # Set LoRa for Europe Region

# creating OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0028908')#
app_key = ubinascii.unhexlify('7C4AB401DA0A3E3DC8BA82D6659E96DE')#

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

#wait until the module has joined the network
while not lora.has_joined():
    utime.sleep(2.5)
    print('Not yet joined...')
    pycom.rgbled(off)

# we're online, set LED to green and notify via print
pycom.rgbled(0x007f00)
print('Network joined!')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


# make the socket non-blocking
# because if there's no data received it will block forever...
s.setblocking(False)
s.bind(1)

# open the RTC
rtc = RTC()
now = rtc.now()

# send some data
while True:
    temperature = int(abs(random()*100))
    print("temperature:", temperature)
    humidity = int(abs(random()*100 - 40))
    print("humidity:", humidity)
    ambient_light = int(abs(random()*100))
    print("ambient_light:", ambient_light)
    pressure = int(abs(random() * 25))
    print("pressure:", pressure)

    
    try:
        packet = ustruct.pack('hhhh', temperature, humidity, ambient_light, pressure)
        print(packet)
        s.send(packet)
        print("Sensor values sent to gateway: ", ustruct.unpack('hhhh', packet))
    except OSError as e:
        if e.args[0] == 11:
            utime.sleep(2.5)
            pycom.rgbled(0x7f0000)
            s.send(packet) #red

    else:
        pycom.rgbled(0x7f7f00) #yellow

	utime.sleep(1)
	pycom.rgbled(0x007f00) #green
	utime.sleep(9)
