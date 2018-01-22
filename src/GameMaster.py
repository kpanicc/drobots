#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I"C:\Program Files (x86)\ZeroC\Ice-3.6.4\slice\" --all drobotsRender.ice')
#Ice.loadSlice("-I/usr/share/Ice-3.6.4/slice/ --all drobotsRender.ice")
#Ice.loadSlice("-I/usr/share/ice/slice/ --all drobotsRender.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm

class GameObserverI(drobotscomm.GameObserver):
    def __init__(self, canvas, observableprx):
        self.canvas = canvas
        self.observableprx = observableprx
        self.identity = None

    def getrobots(self, current):
        if self.canvas is None or self.canvas.bots is None:
            return []

        robotpos = []
        for robot in self.canvas.bots:
            if robot.damage != 100:
                robotpos.append(drobots.Point(robot.x, robot.y))
        return robotpos

    def changeGameServer(self, gameserver, current):
        if self.identity is None:
            self.identity = current.adapter.getCommunicator().stringToIdentity("icanvas")
            print("Identity {}  created".format(self.identity))

        locator = current.adapter.getCommunicator().propertyToProxy("GameName.Locator")
        locator = Ice.LocatorPrx.checkedCast(locator)

        gameserver = current.adapter.getCommunicator().stringToProxy(gameserver)
        gameserver = gameserver.ice_locator(locator)

        servant = CanvasI()
        if self.observableprx is not None:
            current.adapter.remove(self.identity)

        #canvas_proxy = current.adapter.addWithUUID(servant)
        canvas_proxy = current.adapter.add(servant, self.identity)

        game = drobots.ObservablePrx.checkedCast(gameserver)
        connection = game.ice_getCachedConnection()
        connection.setAdapter(current.adapter)

        game.attach(canvas_proxy.ice_getIdentity())

        self.canvas = servant
        self.observableprx = game

        print("GameObserver set to observe game {}  with servant UUID: {}  and locator {}".format(gameserver, canvas_proxy, locator))


class CanvasI(drobots.GameObserver.Canvas):
    def __init__(self):
        self.bots = None
        self.missiles = None
        self.explosions = None
        self.scans = None

    def clean(self, current):
        self.bots = None
        self.missiles = None
        self.explosions = None
        self.scans = None
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
        broker = self.communicator()
        
        props = broker.getProperties()

        # game_proxy = broker.propertyToProxy("GameName")

        adapter = broker.createObjectAdapter(props.getProperty("Name"))
        """servant = CanvasI()
        canvas_proxy = adapter.addWithUUID(servant)

        game = drobots.ObservablePrx.checkedCast(game_proxy)
        connection = game.ice_getCachedConnection()
        connection.setAdapter(adapter)

        game.attach(canvas_proxy.ice_getIdentity())"""

        # Our object
        servant = GameObserverI(None, None)
        observer_proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("ObserverName")))

        #print("Canvas proxy: {}".format(canvas_proxy))
        print("Observer proxy: {}".format(observer_proxy))

        adapter.activate()

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

 
if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))
