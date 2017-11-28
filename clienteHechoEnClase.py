#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

#PREGUNTAR: 5 terminales. Mismo puerto en las 3 instancias. 3 Ice.Applications


import sys
import random
import Ice
from detectorControllerenClase import DetectorControllerI
from robotController import RobotControllerI
Ice.loadSlice('drobots.ice')
import drobots


class PlayerI(drobots.Player):
    def __init__(self):
        self.mines = []
        self.detectorController = None

    def makeController(self, current):
        controller = RobotControllerI()
        prx = current.adapter.addWithUUID(controller)
        return drobots.RobotControllerPrx.uncheckedCast(prx)

    def makeDetectorController(self, current):
        if self.detectorController is None:
            controller = DetectorControllerI()
            object_prx = current.adapter.addWithUUID(controller)
            self.detectorController = drobots.DetectorControllerPrx.CheckedCast(object_prx)
        return self.detectorController

    def getMinePosition(self, bot, current):
        x = random.randint(0, 399)
        y = random.randint(0, 399)
        pos = drobots.Point(x, y)

        while pos in self.mines:
            x = random.randint(0, 399)
            y = random.randint(0, 399)
            pos = drobots.Point(x, y)
            self.mines.append(pos)

        self.mines.append(pos)
        return pos


    def win(self, current):
        print("I win")
        current.adapter.getCommunicator().shutdown()

    def lose(self, current):
        print("I lose")
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current):
        print("Game aborted")
        current.adapter.getCommunicator().shutdown()


class ClientApp(Ice.Application):
    def run(self, args):
        broker = self.communicator()

        adapter = broker.createObjectAdapter("PlayerAdapter")

        servant = PlayerI()

        playerPrx = adapter.addWithUUID(servant)
        playerPrx = drobots.PlayerPrx.uncheckedCast(playerPrx)

        print(playerPrx)

        prx = broker.propertyToProxy("GameProxy")

        adapter.activate()
        name = broker.getProperties().getProperty("PlayerName")
        game_prx = drobots.GamePrx.uncheckedCast(prx)
        game_prx.login(playerPrx, name)



        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        
if __name__ == "__main__":
    app = ClientApp()
    sys.exit(app.main(sys.argv))
