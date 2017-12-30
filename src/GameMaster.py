#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import hashlib

Ice.loadSlice("-I/usr/share/Ice-3.6.4/slice/ --all drobotsRender.ice")
import drobots
Ice.loadSlice("-I. --all drobotsSlaves.ice")
import drobotsSlaves


class CanvasI(drobots.GameObserver.Canvas):
    def __init__(self):
        pass

    def clean(self, current):
        print("I am cleaning")

    def draw(self, snapshot, current):
        print(snapshot.bots)
        print(snapshot.missiles)
        print(snapshot.explosions)
        print(snapshot.scans)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        proxy = broker.getProperties().getProperty("GameName")

        game_proxy = broker.stringToProxy(proxy)

        adapter = broker.createObjectAdapter(broker.getProperties().getProperty("AdapterName"))

        servant = CanvasI()
        canvas_proxy = adapter.addWithUUID(servant)

        game = drobots.ObservablePrx.uncheckedCast(game_proxy)
        print(canvas_proxy)
        #connection = game.ice_getCachedConnection()
        #connection.setAdapter(adapter)

        game.attach(canvas_proxy.ice_getIdentity())

        print(canvas_proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

    
def replaceConfigFileForCLIArgs(argv): 
    configs = list(filter(lambda x: '--Ice.Config' in x, argv)) 
    if len(configs) is not 1: 
        return argv 
    arg = configs[0] 
    path = arg[arg.index("=") + 1:] 
 
    filec = None 
    with open(path, "r") as f: 
        filec = f.read() 
 
    arglist = [] 
    for l in filec.splitlines(): 
        if l.startswith("Ice.Admin.ServerId"): # Do the magic 
            continue 
        if len(l) != 0 and l[0] != "#": 
            arglist.append("--" + l) 
 
    finalargv = [] 
    for a in argv: 
        if a != arg: 
            finalargv.append(a) 
        else: 
            for i in arglist: 
                finalargv.append(i) 
 
    return finalargv 
 
if __name__ == "__main__": 
    sys.argv = replaceConfigFileForCLIArgs(sys.argv) 
    server = Server() 
    sys.exit(server.main(sys.argv))
