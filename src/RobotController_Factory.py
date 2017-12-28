#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm
Ice.loadSlice("-I. --all drobotsSlaves.ice")
import drobotsSlaves

from robotControllers import RobotControllerDefI, RobotControllerAttI


class RobotFactory(drobotscomm.RBFactory):
    def makeRobotController(self, name, bot, current):

        if bot.ice_isA("::drobots::Defender"):
            servant = RobotControllerDefI(bot, name)
            print("invoked make controller name {} type defender".format(name))
            sys.stdout.flush()
        else:  # Robot is an attacker or total, but we only need attackers
            servant = RobotControllerAttI(bot, name)
            print("invoked make controller name {} type attacker".format(name))
            sys.stdout.flush()

        proxy = current.adapter.addWithUUID(servant)
        proxy = current.adapter.createDirectProxy(proxy.ice_getIdentity())

        if not bot.ice_isA("::drobots::Defender"):
            print("Attempting to link to container robot {}".format(name))
            sys.stdout.flush()
            containerprx = current.adapter.getCommunicator().propertyToProxy("RobotContainer")
            print("casting")
            sys.stdout.flush()
            containerprx = drobotscomm.AttRobotContainerPrx.checkedCast(containerprx)
            print("linking")
            sys.stdout.flush()

            containerprx.link(name, drobotsSlaves.robotControllerAttackerSlavePrx.checkedCast(proxy))

        print("returning proxy")
        sys.stdout.flush()
        proxy = drobots.RobotControllerPrx.checkedCast(proxy)
        return proxy


class Server_RF(Ice.Application):
    def run(self, args):
        broker = self.communicator()

        props = self.communicator().getProperties()

        servant = RobotFactory()
        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))
        proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))
        print(proxy)
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()

        containerprx = broker.propertyToProxy("FactoryContainer")
        containerprx = drobotscomm.FactoryContainerPrx.checkedCast(containerprx)

        containerprx.link(props.getProperty("Name"), drobotscomm.RBFactoryPrx.uncheckedCast(proxy))
        broker.waitForShutdown()
        containerprx.unlink(props.getProperty("Name"))


if __name__ == "__main__":
    app = Server_RF()
    sys.exit(app.main(sys.argv))
