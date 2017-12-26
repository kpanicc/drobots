#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-



import sys
import random
import Ice
from DetectorController import DetectorControllerI
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("drobotscomm.ice")
import drobotscomm


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

        print("invoked make controller time {}".format(self.i))
        sys.stdout.flush()
        containerprx = current.adapter.getCommunicator().propertyToProxy("Container")
        containerprx = drobotscomm.FactoryContainerPrx.checkedCast(containerprx)

        self.factories = containerprx.list()
        props = current.adapter.getCommunicator().getProperties()
        self.i += 1
        currentFactory = self.factories[props.getProperty("ControllerFactory{}".format(self.i))]


        controllerprx = currentFactory.makeRobotController("robot{}".format(self.i), bot)

        print(controllerprx)
        sys.stdout.flush()
        return controllerprx


    def makeDetectorController(self, current):
        if self.detectorController is None:
            controller = DetectorControllerI()
            object_prx = current.adapter.addWithUUID(controller)
            object_prx = current.adapter.createDirectProxy(object_prx.ice_getIdentity())
            self.detectorController = drobots.DetectorControllerPrx.checkedCast(object_prx)
        return self.detectorController

    def getMinePosition(self, current):
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

        Game_Factory_prx = broker.propertyToProxy("GameFactory")
        Game_Factory_prx = drobots.GameFactoryPrx.checkedCast(Game_Factory_prx)

        #game_prx = broker.propertyToProxy("GameProxy")
        game_prx = Game_Factory_prx.makeGame(props.getProperty("GameName"), int(props.getProperty("GameNPlayers")))
        game_prx = drobots.GamePrx.uncheckedCast(game_prx)

        name = broker.getProperties().getProperty("Name")

        servant = PlayerI()
        playerPrx = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        playerPrx = adapter.createDirectProxy(playerPrx.ice_getIdentity())
        playerPrx = drobots.PlayerPrx.uncheckedCast(playerPrx)

        adapter.activate()

        print("Connecting to game {} with nickname {}".format(game_prx, name))
        sys.stdout.flush()

        game_prx.login(playerPrx, name)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        
if __name__ == "__main__":
    try:
        app = ClientApp()
        sys.exit(app.main(sys.argv))
    except Exception as e:
        print(e)