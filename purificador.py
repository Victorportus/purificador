import time
import board
import busio
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
'''Se usa repositorio adafruit para poder leer la informacion del sensor.
Esta debe ser instalada desde consola "sudo pip3 install adafruit-circuitpython-dht"
Y "sudo apt install python3-libgpiod"'''
import adafruit_dht
'''En terminal, instalar "sudo pip3 install adafruit-circuitpython-tsl2561"'''
import adafruit_tsl2561
'''urllib, se usa para conectarse con URL, en este caso thingspeak'''
import urllib.request

class Purificador():    
    def __init__(self, pin=21):
        while True:
            try:
                self.ledOn(pin)
                tsl, dht = self.connect()
                self.readSensors(tsl, dht)
                self.load()           
                self.ledOff(pin)
                '''Cambiar el time sleep sgun cada cuanto se quiera tomar la data. Tiempo en segundos.'''
                time.sleep(60.0)
            except:
                self.closeDht(dht)
                self.ledOff(21)
                print ("Fail to upload" )
                sys.exit(0)
            
    def connect(self):
        tsl = self.connectTsl()
        dht = self.connectDht()
        return tsl, dht
        
    def connectTsl(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_tsl2561.TSL2561(i2c)
        return sensor
    
    def connectDht(self):
        '''board.D4, se refiere al pin al que esta coenctado el sensor DHT22,si se conecta a uno diferente se debe cambiar'''
        dht = adafruit_dht.DHT22(board.D4)
        return dht
    
    # Metodo usado para leer sensor DHT22
    def dht(self, dht):
        while True:
            try:
                temperature = dht.temperature
                humidity = dht.humidity
                break
            except RuntimeError as error:
                time.sleep(2.0)
                continue
        self.setTemp(temperature)
        self.setHumi(humidity)
        
    # Metodo para leer sensor Tsl2561
    def tsl(self, tsl):
        lux = tsl.lux
        broad = tsl.broadband
        infra = tsl.infrared
        lumi = tsl.luminosity
        self.setLux(lux)
        
    def readSensors(self, tsl, dht):
        self.tsl(tsl)
        self.dht(dht)
        self.closeDht(dht)
    
    def load(self):
        self.loadLux()
        time.sleep(15.0)
        self.loadTemp()
        time.sleep(15.0)
        self.loadHumi()
    
    # Load data into thingspeak
    '''Para subir la data a thingspeak se debe crear la cuenta y un canal, con 3 campos.
    En el primero se cargar la data de luxos, en el segundo la temperatura y en el tercero la humedad.
    Una vez creado el canal, verificar la API key, para enviar la data a su canal.
    ES MUY IMPORTANTE CAMBIAR EL KEY EN LOS 3 METODOS DE LOAD PARA PODER SUBIRLA A SU CANAL, DE LO CONTRARIO SE SUBIRA AL MIO.
    Al final de cada direccion, se debe verificar que corresponda al "field" adecuado, asi como esta actualmente.'''
    def loadLux(self):
        loadLux = "https://api.thingspeak.com/update?api_key=9W528L3P4KAO5YVR&field1="
        f = urllib.request.urlopen(loadLux + str(self.getLux()))
        f.read()
        f.close()
    def loadTemp(self):
        loadTemp = "https://api.thingspeak.com/update?api_key=9W528L3P4KAO5YVR&field2="
        f = urllib.request.urlopen(loadTemp + str(self.getTemp()))
        f.read()
        f.close()
    def loadHumi(self):
        loadHumi = "https://api.thingspeak.com/update?api_key=9W528L3P4KAO5YVR&field3="
        f = urllib.request.urlopen(loadHumi + str(self.getHumi()))
        f.read()
        f.close()
        
    # Prender led en GPIO21
    def ledOn(self, l):
        GPIO.setup(l, GPIO.OUT)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(l, GPIO.HIGH)
        
    # Apagar led en GPIO21
    def ledOff(slef, l):
        GPIO.output(l, GPIO.LOW)
        
    def closeDht(self, dht):
        dht.exit()
        
    def getTemp(self):
        return self.temp
    def setTemp(self, p):
        self.temp = p
        
    def getHumi(self):
        return self.humi
    def setHumi(self, p):
        self.humi = p
        
    def getLux(self):
        return self.lux
    def setLux(self, p):
        self.lux = p
        
if __name__ == "__main__":
    purificador = Purificador()

