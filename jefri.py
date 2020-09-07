import RPi.GPIO as GPIO
import time
import sqlite3
import datetime

class Led:

        def __init__(self,pin):
                self.ledPin = pin
                self.status = False
                GPIO.setup(pin,GPIO.OUT)

        def ledAn(self):
                GPIO.output(self.ledPin, GPIO.HIGH)
                self.status = True

        def ledAus(self):
                GPIO.output(self.ledPin, GPIO.LOW)
                self.status = False

class Taster:

        def __init__(self,pin):
                self.tasterPin = pin
                self.status = 0
                GPIO.setup(pin, GPIO.IN)

        def checkTaster(self):
                if GPIO.input(self.tasterPin):
                        self.status = True
                        return True

                else:
                        return False
                        self.status = False

class DB:

        def __init__(self):
                self.conn = sqlite3.connect('zeit.db')
                self.c = self.conn.cursor()

        def erstelleDatenbank(self):
                self.c.execute('''CREATE TABLE Zeitwerte
                             (zeitstempel, led_zustand )''')

                self.conn.commit()

        def schreiben(self, zeit, led_zustand):
                self.c.execute("INSERT INTO Zeitwerte VALUES ('" + zeit + "','" + led_zustand + "')")
                self.conn.commit()


class Main:

        def __init__(self):
                GPIO.setmode(GPIO.BOARD)
                self.taster = Taster(13)
                self.led = Led(11)
                self.DB = DB()

        def controll(self):
                if self.taster.checkTaster():
                        x = datetime.datetime.now()
                        print(x)
                        while self.taster.status == True:
                                time.sleep(0.3)
                                if self.taster.checkTaster() == False:
                                        break

                        y = datetime.datetime.now()
                        zeit = y-x
                        print(zeit)
                        if zeit.seconds > 0: # alles was ueber eine Sekunde ist
                                pass

                        else:
                                if self.led.status == False:
                                        self.led.ledAn()
                                        self.DB.schreiben(time.asctime(time.localtime(time.time())), "LED an")

                                else:
                                        self.led.ledAus()
                                        self.DB.schreiben(time.asctime(time.localtime(time.time())), "LED aus")


try:

        DB().erstelleDatenbank()
        
except sqlite3.OperationalError:
        pass
        
Start = Main()
try:

        while True:
                Start.controll()

except: KeyboardInterrupt





time.sleep(0.5)
GPIO.cleanup()

