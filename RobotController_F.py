#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys
Ice.loadSlice('drobots.ice')
Ice.loadSlice('-I. --all FactoryContainer.ice')
import drobots


class RobotControllerI(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot

    def turn(self, current):
        print(self.bot.location())

    def robotDestroyed(self, current):
        print("robot destroyed")


class RB_Factory(drobots.RBFactory):
    def makeRobotController(self, name, bot, current):
        servant = RobotControllerI(bot)
        proxy = current.adapter.addWithUUID(servant)
        proxy_id = proxy.ice_getIdentity()
        direct_proxy = current.adapter.createDirectProxy(proxy_id)
        return drobots.RobotControllerPrx.uncheckedCast(direct_proxy)


class Server_RF(Ice.Application):
    def run(self, args):
        broker = self.communicator()

        containerprx = broker.propertyToProxy("Container")
        containerprx = drobots.FactoryContainerPrx.checkedCast(containerprx)

        props = self.communicator().getProperties()

        servant = RB_Factory()
        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))
        proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        print(proxy)
        adapter.activate()
        self.shutdownOnInterrupt()

        containerprx.link(props.getProperty("Name"), drobots.RBFactoryPrx.uncheckedCast(proxy))
        broker.waitForShutdown()
        containerprx.unlink(props.getProperty("Name"))


if __name__ == "__main__":
    app = Server_RF()
    sys.exit(app.main(sys.argv))
