#pinger.py
#System modules
import os
import json
from dotenv import load_dotenv
import threading
import time
from collections import deque

from ping3 import ping

load_dotenv()

ADDRESSES_TO_PING = json.loads(os.getenv('ADDRESSES_TO_PING'))


class DelayMessage:
    address = ''
    averageDelay = 0.0
    def __init__(self, address, averageDelay) -> None:
        self.address = address
        self.averageDelay = averageDelay

#helper PingTarget class 
class PingTarget:
    address = ''
    pingDelays = deque()

    def __init__(self, addr) -> None:
        self.address = addr
        self.pingDelays = deque()

    def getAverageDelay(self) -> float:
        #Error check, are there values?

        if len(self.pingDelays) == 0:
            return 9999.0
        else:
            tmp = 0.0
            for delay in self.pingDelays:
                tmp += delay
            return tmp / len(self.pingDelays)
#PingTarget!

#Main Pinger threaded class
class Pinger(threading.Thread):
    listMaxLength = 43200 # 60s*60m*12h
    pingTargets = []

    def __initialize(self) -> None:
        for i in range(len(ADDRESSES_TO_PING)):
            self.pingTargets.append(PingTarget(addr=ADDRESSES_TO_PING[i]))

    def __mainPingLoop(self) -> None:
        while True:
                    time.sleep(1)
                    for target in self.pingTargets:
                        delay = ping(target.address, timeout = 4)   #in milliseconds
                        if delay == False or delay == None:
                            print('Failed to ping '+ str(target.address))
                            delay = 4*1000 # 4 seconds
                        self.addPingResult(target, delay*1000) #for ms
                    self.printAverage()

    def addPingResult(self, target, delay):
        print(str(str(target.address)) + " delay: "+str(delay))
        target.pingDelays.append(delay)
        if len(target.pingDelays) >= self.listMaxLength:
            target.pingDelays.popleft()

    def printAverage(self):
        for target in self.pingTargets:     
            average = target.getAverageDelay()
            print(target.address +": average ping time is: " + str(average) + "out of a sample of " + str(len(target.pingDelays)))


    def getAverage(self):
        delays = [] #hodls the values
        for target in self.pingTargets:     
            average = target.getAverageDelay()
            delays.append(DelayMessage(target.address,average))
        return delays

    def run(self):
        self.__initialize()
        self.__mainPingLoop()
#Pinger!
