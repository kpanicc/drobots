#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
from time import time

Ice.loadSlice("-I/usr/share/Ice-3.6.4/slice/ --all drobotsRender.ice")
#Ice.loadSlice("-I/usr/share/ice/slice/ --all drobotsRender.ice")
import drobots
Ice.loadSlice("-I. --all drobotsSlaves.ice")
import drobotsSlaves
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm


class CanvasI(drobots.GameObserver.Canvas):
    def __init__(self):
        self.timedelta = 0.2
        self.lastupdate = time()
        self.robots = None
        self.containerPrx = None

    def clean(self, current):
        print("I am cleaning")

    def draw(self, snapshot, current):
        print(snapshot.bots)
        print(snapshot.missiles)
        print(snapshot.explosions)
        print(snapshot.scans)

        # We may get updates every time the server ticks, which may collapse the bots
        if (time() - self.lastupdate) > self.timedelta:
            self.lastupdate = time()

            if self.containerPrx is None: # Get the robot container
                self.containerPrx = current.adapter.getCommunicator().propertyToProxy("Container")
                self.containerPrx = drobotscomm.AttRobotContainerPrx.checkedCast(self.containerPrx)

            if self.robots is None:
                self.robots = self.containerPrx.list().values  # Get all robots (and keep only the proxies)

            for robot in self.robots:
                if robot.ice_isA("::drobots::Attacker"):  # Send the points to attackers only
                    dpoints = []
                    for bot in snapshot.bots:
                        dpoint = drobots.Point(bot.x, bot.y)
                        dpoints.append(dpoint)

                    robot.receiveOrders(dpoints)



class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        atclabLocatorProxy = broker.propertyToProxy("GameName.Locator")
        atclabLocatorObject = Ice.LocatorPrx.checkedCast(atclabLocatorProxy)

        proxy = broker.getProperties().getProperty("GameName")

        game_proxy = broker.stringToProxy(proxy)
        game_proxy = game_proxy.ice_locator(atclabLocatorObject)

        adapter = broker.createObjectAdapter("")

        servant = CanvasI()
        canvas_proxy = adapter.addWithUUID(servant)

        print("Game Proxy locator: " + str(game_proxy.ice_getLocator()))
        print("Adapter locator: " + str(adapter.getLocator()))
        game = drobots.ObservablePrx.checkedCast(game_proxy)

        game.attach(canvas_proxy.ice_getIdentity())

        ouradapter = broker.createObjectAdapter(broker.getProperties().getProperty("Name"))

        print(canvas_proxy)
        sys.stdout.flush()

        adapter.activate()
        ouradapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

 
if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))
