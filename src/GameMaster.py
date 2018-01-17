#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
from time import time

Ice.loadSlice("-I/usr/share/Ice-3.6.4/slice/ --all drobotsRender.ice")
#Ice.loadSlice("-I/usr/share/ice/slice/ --all drobotsRender.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm

class GameObserverI(drobotscomm.GameObserver):
    def __init__(self, canvas):
        self.canvas = canvas

    def getrobots(self, current):
        robotpos = []
        for robot in self.canvas.bots:
            if robot.damage != 100:
                robotpos.append(drobots.Point(robot.x, robot.y))
        return robotpos

class CanvasI(drobots.GameObserver.Canvas):
    def __init__(self):
        self.bots = None
        self.missiles = None
        self.explosions = None
        self.scans = None

    def clean(self, current):
        print("I am cleaning")

    def draw(self, snapshot, current):
        self.bots = snapshot.bots
        self.missiles = snapshot.missiles
        self.explosions = snapshot.explosions
        self.scans = snapshot.scans
        print("Updated")
        sys.stdout.flush()



class Server(Ice.Application):
    def run(self, argv):
        """broker = self.communicator()

        atclabLocatorProxy = broker.propertyToProxy("GameName.Locator")
        atclabLocatorObject = Ice.LocatorPrx.checkedCast(atclabLocatorProxy)

        proxy = props.getProperty("GameName")

        game_proxy = broker.stringToProxy(proxy)
        game_proxy = game_proxy.ice_locator(atclabLocatorObject)

        adapter = broker.createObjectAdapter("")

        servant = CanvasI()
        canvas_proxy = adapter.addWithUUID(servant)

        game = drobots.ObservablePrx.checkedCast(game_proxy)

        game.attach(canvas_proxy.ice_getIdentity())

        # Our gameobserver code
        ouradapter = broker.createObjectAdapter(props.getProperty("Name"))
        ourservant = GameObserverI(servant)
        our_proxy = ouradapter.addWithUUID(ourservant)

        print(canvas_proxy)
        sys.stdout.flush()

        print("Game Proxy locator: " + str(game_proxy.ice_getLocator()))
        print("Adapter locator: " + str(adapter.getLocator()))
        print("Canvas proxy: " + str(canvas_proxy))
        print("GameObserver proxy: " + str(our_proxy))

        adapter.activate()
        ouradapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0"""

        broker = self.communicator()
        
        props = broker.getProperties()

        game_proxy = broker.propertyToProxy("GameName")

        adapter = broker.createObjectAdapter(props.getProperty("Name"))
        servant = CanvasI()
        canvas_proxy = adapter.addWithUUID(servant)

        game = drobots.ObservablePrx.checkedCast(game_proxy)
        connection = game.ice_getCachedConnection()
        connection.setAdapter(adapter)

        game.attach(canvas_proxy.ice_getIdentity())

        # Our object
        servant = GameObserverI(servant)
        observer_proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("ObserverName")))

        print("Canvas proxy: {}".format(canvas_proxy))
        print("Observer proxy: {}".format(observer_proxy))

        adapter.activate()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

 
if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))
