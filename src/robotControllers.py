#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm


class RobotControllerDefI(drobots.RobotController):
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def turn(self, current):
        location = self.bot.location()
        print("Turn of {} at location {},{}".format(
            id(self), location.x, location.y))
        sys.stdout.flush()

    def robotDestroyed(self, current):
        print("robot destroyed")
        sys.stdout.flush()


class RobotControllerAttI(drobotscomm.RobotControllerSlave):
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
        self.orders = []
        self.location = None
        self.energy = 100
        self.destroyed = False
        self.speed = 0
        self.life = 100
        self.destroyed = False
        self.robotcontainer = None
        self.gameobserverprx = None

        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def getLocation(self):
        return self.location

    def turn(self, current):
        if self.destroyed:
            return

        if not self.location:
            self.getlocation()

        if self.robotcontainer is None:
            containerprx = current.adapter.getCommunicator().propertyToProxy("Container")
            self.robotcontainer = drobotscomm.RobotContainerPrx.checkedCast(containerprx)
            print("Robot Container obtained")
            sys.stdout.flush()

        if self.gameobserverprx is None:
            self.gameobserverprx = current.adapter.getCommunicator().propertyToProxy("GameObserver")
            self.gameobserverprx = drobotscomm.GameObserverPrx.checkedCast(self.gameobserverprx)
            print("Game Observer obtained")
            sys.stdout.flush()

        gamerobotspromise = self.gameobserverprx.begin_getrobots()

        ourobotslocation = self.robotcontainer.list()
        ourobotslocation = list(map(lambda x: x.getLocation(), ourobotslocation.values()))

        gamerobots = self.gameobserverprx.end_getrobots(gamerobotspromise)  # AMD

        for robot in gamerobots:
            if robot not in ourobotslocation:
                if self.canshoot():
                    self.shoot(robot)

        self.energy = 100
        print("Turn of {} at location {},{}".format(
            id(self), self.location.x, self.location.y))
        sys.stdout.flush()

    def getlocation(self):
        print("Bot {} asked for its location".format(self.bot))
        sys.stdout.flush()
        self.location = self.bot.location()
        self.energy -= 1

    def canshoot(self):
        return self.energy >= 50

    def shoot(self, position):
        print("Bot {} shooting at {},{}".format(self.bot, position.x, position.y))
        sys.stdout.flush()
        self.bot.cannon(self.calculateAngle(position), self.calculateDistance(position))
        self.energy -= 50

    def robotDestroyed(self, current):
        self.destroyed = True
        print("robot destroyed")
        sys.stdout.flush()

    def calculateDistance(self, point):
        return math.sqrt(math.pow((self.location.x - point.x), 2) +
                         math.pow((self.location.y - point.y), 2))
#       return euclidean distance to point

    def calculateAngle(self, point):
        vector = [point.x - self.location.x, point.y - self.location.y]

        # TODO: Replace math.pow by **
        angle = vector[0] / (math.sqrt(1 + math.pow(vector[0], 2)) + math.sqrt(math.pow(vector[1], 2)))
#       This angle is the shortest angle between the direction to the point and the east(0 degrees angle)
#       If the point is lower to the location, the angle will be 360 - angle

        if point.x < self.location.x:
            angle = 360 - angle

        return int(angle)
