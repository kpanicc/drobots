#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-



import sys
import random
import Ice
from DetectorController import DetectorControllerI
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm


class PlayerI(drobots.Player):
    def __init__(self):
        self.mines = []
        self.i = 0
        self.controllerFactory = None

    def resetState(self, broker):
        print("Resetting state")
        sys.stdout.flush()
        robotcontainerprx = broker.propertyToProxy("RobotContainer")
        robotcontainerprx = drobotscomm.RobotContainerPrx.checkedCast(robotcontainerprx)
        robotcontainerprx.flush()

        if self.controllerFactory is not None:
            self.controllerFactory.resetCount()
        else:
            dFactory = broker.propertyToProxy("DetectorFactoryProxy")
            dFactory = drobotscomm.ControllerFactoryPrx.checkedCast(dFactory)
            dFactory.resetCount()

        detectorcontainerprx = broker.propertyToProxy("DetectorContainer")
        detectorcontainerprx = drobotscomm.DetectorContainerPrx.checkedCast(detectorcontainerprx)
        detectorcontainerprx.flush()

        print("State has been reset")

    def makeController(self, bot, current):
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
        print("Getting detector factory")
        dFactory = current.adapter.getCommunicator().propertyToProxy("DetectorFactoryProxy")
        print("Indirect factory proxy: {}".format(dFactory))
        print("Indirect proxy identity: {}".format(dFactory.ice_getIdentity()))
        sys.stdout.flush()

        dFactory = drobotscomm.ControllerFactoryPrx.checkedCast(dFactory)
        self.controllerFactory = dFactory
        print("Factory casted")

        dController = dFactory.makeDetectorController()
        print("Controller returned")
        return dController

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
        sys.stdout.flush()
        self.resetState(current.adapter.getCommunicator())
        current.adapter.getCommunicator().shutdown()

    def lose(self, current):
        print("I lose")
        sys.stdout.flush()
        self.resetState(current.adapter.getCommunicator())
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current):
        print("Game aborted")
        sys.stdout.flush()
        self.resetState(current.adapter.getCommunicator())
        current.adapter.getCommunicator().shutdown()


class ClientApp(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        props = self.communicator().getProperties()

        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))

        Game_Factory_prx = broker.propertyToProxy("GameFactory")
        Game_Factory_prx = drobots.GameFactoryPrx.checkedCast(Game_Factory_prx)

        wkProxy = False
        gamename = broker.getProperties().getProperty("GameProxy")
        if gamename.startswith("drobots"):
            try:
                gamename = int(gamename[len("drobots"):])
                if gamename in range(16):
                    wkProxy = True
                else:
                    wkProxy = False
            except:
                wkProxy = False

        if wkProxy:
            game_prx = broker.propertyToProxy("GameProxy")
        else:
            game_prx = Game_Factory_prx.makeGame(props.getProperty("GameProxy"), int(props.getProperty("GameNPlayers")))

        game_prx = drobots.GamePrx.uncheckedCast(game_prx)

        name = broker.getProperties().getProperty("PlayerName")

        servant = PlayerI()
        playerPrx = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        playerPrx = adapter.createDirectProxy(playerPrx.ice_getIdentity())
        playerPrx = drobots.PlayerPrx.uncheckedCast(playerPrx)

        adapter.activate()

        print("Connecting to game {} with nickname {}".format(game_prx, name))
        sys.stdout.flush()

        self.setGameObserverGame(broker)

        game_prx.login(playerPrx, name)

        self.shutdownOnInterrupt()
        broker.waitForShutdown()

    def setGameObserverGame(self, broker):
        gameobserverprx = broker.propertyToProxy("GameObserver")
        gameobserverprx = drobotscomm.GameObserverPrx.checkedCast(gameobserverprx)

        gameobserverprx.changeGameServer(broker.getProperties().getProperty("GameProxy"))


if __name__ == "__main__":
    try:
        app = ClientApp()
        sys.exit(app.main(sys.argv))
    except Exception as e:
        print(e)
