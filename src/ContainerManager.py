#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys

import Ice
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm

class FactoryContainer(drobotscomm.FactoryContainer):
    def __init__(self):
        self.factories = {}

    def link(self, key, proxy, current):
        if key in self.factories:
            raise drobotscomm.AlreadyExists("key: {}".format(key))
        else:
            self.factories[key] = proxy
            print("linking factory {} with key {}".format(proxy, key))
            sys.stdout.flush()

    def unlink(self, key, current):
        if key not in self.factories:
            raise drobotscomm.NoSuchKey("key: {}".format(key))
        else:
            del self.factories[key]

    def list(self, current):
        print("listing factories")
        sys.stdout.flush()
        return self.factories


class RobotContainer(drobotscomm.AttRobotContainer):
    def __init__(self):
        self.robots = {}

    def link(self, key, proxy, current):
        if key in self.robots:
            raise drobotscomm.AlreadyExists("key: {}".format(key))
        else:
            self.robots[key] = proxy
            print("linking Robot {} with key {}".format(proxy, key))
            sys.stdout.flush()

    def unlink(self, key, current):
        if key not in self.robots:
            raise drobotscomm.NoSuchKey("key: {}".format(key))
        else:
            del self.robots[key]

    def list(self, current):
        print("listing robots")
        sys.stdout.flush()
        return self.robots


class ContainerStart(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servantFactory = FactoryContainer()
        servantRobot = RobotContainer()

        props = self.communicator().getProperties()
        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))
        proxyFactory = adapter.add(servantFactory, broker.stringToIdentity(props.getProperty("FactoryCName")))

        proxyRobot = adapter.add(servantRobot, broker.stringToIdentity(props.getProperty("RobotCName")))

        print(proxyFactory)
        print(proxyRobot)
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == "__main__":
    app = ContainerStart()
    sys.exit(app.main(sys.argv))




