#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys
Ice.loadSlice('drobots_final.ice')
import drobots


class RobotControllerI(drobots.RobotController):
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def turn(self, current):
        print(self.bot.location())

    def robotDestroyed(self, current):
        print("robot destroyed")

    def print(self, current):
        print(repr(self.bot))
        print("\n\n\n\n\n")
        sys.stdout.flush()


class RB_Factory(drobots.RBFactory):
    def makeRobotController(self, name, bot, current):
        servant = RobotControllerI(bot, name)
        servant.print(current)
        proxy = current.adapter.addWithUUID(servant)
        direct_proxy = current.adapter.createDirectProxy(proxy.ice_getIdentity())

        print("made a direct proxy {}".format(repr(direct_proxy)))
        sys.stdout.flush()

        controller_prx = drobots.RobotControllerPrx.checkedCast(direct_proxy)

        print("invoked make controller name {}".format(name))
        return controller_prx


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
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()

        containerprx.link(props.getProperty("Name"), drobots.RBFactoryPrx.uncheckedCast(proxy))
        broker.waitForShutdown()
        containerprx.unlink(props.getProperty("Name"))


if __name__ == "__main__":
    try:
        app = Server_RF()
        sys.exit(app.main(sys.argv))
    except Exception as e:
        print(e)
        sys.stdout.flush()
