#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("drobotscomm.ice")
import drobotscomm

from robotControllers import RobotControllerTotalI, RobotControllerDefI, RobotControllerAttI


class Robot_Factory(drobotscomm.RBFactory):
    def makeRobotController(self, name, bot, current):

        if bot.ice_isA("::drobots::Defender") and bot.ice_isA("::drobots::Attacker"):
            servant = RobotControllerTotalI(bot, name)
        elif bot.ice_isA("::drobots::Defender"):
            servant = RobotControllerDefI(bot, name)
        else:  # Robot is an attacker
            servant = RobotControllerAttI(bot, name)

        proxy = current.adapter.addWithUUID(servant)
        proxy = current.adapter.createDirectProxy(proxy.ice_getIdentity())

        proxy = drobots.RobotControllerPrx.checkedCast(proxy)



        print("invoked make controller name {}".format(name))
        return proxy


class Server_RF(Ice.Application):
    def run(self, args):
        broker = self.communicator()

        props = self.communicator().getProperties()

        servant = Robot_Factory()
        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))
        proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        print(proxy)
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()

        containerprx = broker.propertyToProxy("Container")
        containerprx = drobotscomm.FactoryContainerPrx.checkedCast(containerprx)

        containerprx.link(props.getProperty("Name"), drobotscomm.RBFactoryPrx.uncheckedCast(proxy))
        broker.waitForShutdown()
        containerprx.unlink(props.getProperty("Name"))


if __name__ == "__main__":
    try:
        app = Server_RF()
        sys.exit(app.main(sys.argv))
    except Exception as e:
        print(e)
        sys.stdout.flush()
