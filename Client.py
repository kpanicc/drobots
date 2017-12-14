#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

#PREGUNTAR: 5 terminales. Mismo puerto en las 3 instancias. 3 Ice.Applications


import sys
import random
import Ice
from DetectorController import DetectorControllerI
from robotController import RobotControllerI
Ice.loadSlice('-I. --all FactoryContainer.ice')
import drobots


class PlayerI(drobots.Player):
    def __init__(self):
        self.mines = []
        self.detectorController = None
        self.i = 0

    def makeController(self, bot, current):
        '''
        proxy = current.adapter.getCommunicator().propertyToProxy("RB_Factory")
        print(proxy)
        proxy = drobots.RBFactoryPrx.uncheckedCast(proxy)
        prx = proxy.makeRobotController("robot1", bot)
        return drobots.RobotControllerPrx.uncheckedCast(prx)
        '''
        containerprx = current.adapter.getCommunicator().propertyToProxy("Container")
        containerprx = drobots.FactoryContainerPrx.checkedCast(containerprx)

        self.factories = containerprx.list()
        props = current.adapter.getCommunicator().getProperties()
        self.i += 1
        currentFactory = self.factories[props.getProperty("ControllerFactory{}".format(self.i))]


        controllerprx = currentFactory.makeRobotController("robot{}".format(self.i), bot)

        print(controllerprx)
        sys.stdout.flush()
        return drobots.RobotControllerPrx.uncheckedCast(controllerprx)


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
        props = self.communicator().getProperties()

        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))

        game_prx = broker.propertyToProxy("GameProxy")
        game_prx = drobots.GamePrx.uncheckedCast(game_prx)

        name = broker.getProperties().getProperty("PlayerName")

        servant = PlayerI()
        playerPrx = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        playerPrx = adapter.createDirectProxy(playerPrx.ice_getIdentity())
        playerPrx = drobots.PlayerPrx.uncheckedCast(playerPrx)

        adapter.activate()

        game_prx.login(playerPrx, name)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        
if __name__ == "__main__":
    app = ClientApp()
    sys.exit(app.main(sys.argv))
