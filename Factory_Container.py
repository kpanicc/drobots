#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys

import Ice
Ice.loadSlice('-I. --all FactoryContainer.ice')
import drobots

class FacContainer(drobots.FactoryContainer):
    def __init__(self):
        self.factories = {}

    def link(self, key, proxy, current):
        if key in self.factories:
            raise drobots.AlreadyExists("key: {}".format(key))
        else:
            self.factories[key] = proxy
            print("linking factory {} with key {}".format(proxy, key))
            sys.stdout.flush()

    def unlink(self, key, current):
        if key not in self.factories:
            raise drobots.NoSuchKey("key: {}".format(key))
        else:
            del self.factories[key]

    def list(self, current):
        print("listing")
        sys.stdout.flush()
        return self.factories


class ContainerStart(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = FacContainer()

        props = self.communicator().getProperties()
        adapter = broker.createObjectAdapter(props.getProperty("AdapterName"))
        proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")))

        print(proxy)
        sys.stdout.flush()
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == "__main__":
    app = ContainerStart()
    sys.exit(app.main(sys.argv))




