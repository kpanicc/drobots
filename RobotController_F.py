#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys
Ice.loadSlice('drobots.ice')
Ice.loadSlice('-I. --all factories.ice')
import drobots


class RobotControllerI(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot

    def turn(self, current):
        print(self.bot.location())

    def robotDestroyed(self, current):
        print("robot destroyed")


class RB_Factory(drobots.RBFactory):
    def makeRobotController(self,name , bot, current):
        servant = RobotControllerI(bot)
        proxy = current.adapter.add(servant, current.adapter.getCommunicator().stringToIdentity(name))
        return drobots.RobotControllerPrx.uncheckedCast(proxy)


class Server_RF(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = RB_Factory()
        adapter = broker.createObjectAdapter("RB_FactoryAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("RB_Factory1"))
        print(proxy)
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == "__main__":

    app = Server_RF()
    sys.exit(app.main(sys.argv))
