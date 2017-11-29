#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
import sys


class RB_Factory(Ice.Application):
    def run(self, args):
	print("Hello")
        broker = self.communicator()
        adapter = broker.createObjectAdapter("FactoryAdapter")
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == "__main__":

    app = RB_Factory()
    sys.exit(app.main(sys.argv))
