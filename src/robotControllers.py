#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys
import Ice
import math
import random
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("-I. --all drobotscomm.ice")
import drobotscomm


class RobotControllerDefI(drobotscomm.RobotControllerSlave):
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
        self.location = None
        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def getLocation(self, current):
        return self.location

    def turn(self, current):
        self.location = self.bot.location()
        print("Turn of {} at location {},{}".format(
            id(self), self.location.x, self.location.y))
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
        self.counter = 0
        self.moveCounter = -1

        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def getLocation(self, current):
        return self.location

    def turn(self, current):
        if self.destroyed:
            return

        self.getActualLocation()

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

        if self.moveCounter > 0:
            self.moveCounter -= 1

        if self.moveCounter == 0:
            self.bot.drive(0, 0)
            self.energy -= 1

        gamerobotspromise = self.gameobserverprx.begin_getrobots()

        ourobotslocation = self.robotcontainer.list()
        ourobotslocation = list(map(lambda x: x.getLocation(), ourobotslocation.values()))

        for ourRobotsPos in ourobotslocation:
            if ourRobotsPos.x != self.location.x and \
                    ourRobotsPos.y != self.location.y:
                self.shouldMove(ourRobotsPos)

        gamerobots = self.gameobserverprx.end_getrobots(gamerobotspromise)  # AMD

        random.shuffle(gamerobots)

        if self.counter > 0:
            for robotPos in gamerobots:
                companion = False
                for ourRobotsPos in ourobotslocation:
                    if ourRobotsPos.x - 2 <= robotPos.x and ourRobotsPos.x + 2 >= robotPos.x and \
                            ourRobotsPos.y - 2 <= robotPos.y and ourRobotsPos.y + 2 >= robotPos.y:
                        companion = True
                if not companion:
                    print("Attempting to shoot {} from {}, robot {}".format(
                        robotPos, self.location, self.name))
                    sys.stdout.flush()
                    self.shouldMove(robotPos)
                    if self.canshoot():
                        self.shoot(robotPos)


        self.energy = 100

        if self.counter == 0:
            self.counter += 1
        print("Turn of {} at location {},{}".format(
            id(self), self.location.x, self.location.y))
        sys.stdout.flush()

    def getActualLocation(self):
        print("Bot {} asked for its location".format(self.bot))
        sys.stdout.flush()
        self.location = self.bot.location()
        self.energy -= 1

    def shouldMove(self, otherPosition):
        if self.calculateDistance(otherPosition) < 80 and \
                self.moveCounter <= 0: #missiles would hit 2 or more
            angle = self.calculateAngle(otherPosition)

            angle = (angle + 180) % 360 #calculate opposite angle

            if self.energy >= 60:
                print("Moving away from {} with angle {}".format(otherPosition, angle))
                sys.stdout.flush()
                self.bot.drive(angle, 100)
                self.energy -= 60
                self.moveCounter = 10



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
        distance = int(math.sqrt(math.pow((self.location.x - point.x), 2) +
                      math.pow((self.location.y - point.y), 2)))

        print("Calculated distance {}".format(distance))
        sys.stdout.flush()

        return distance
#       return euclidean distance to point

    def calculateAngle(self, point):
        vector = [point.x - self.location.x, point.y - self.location.y]

        angle = math.atan2(vector[1], vector[0]) * (180/math.pi)

        if angle < 0:
            angle += 360

        print("Calculated angle {}".format(angle))
        sys.stdout.flush()

        return int(angle)
