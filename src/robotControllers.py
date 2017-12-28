#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys
import Ice
import math
Ice.loadSlice("drobots.ice")
import drobots
Ice.loadSlice("-I. --all drobotsSlaves.ice")
import drobotsSlaves


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


class RobotControllerAttI(drobotsSlaves.robotControllerAttackerSlave):
    def __init__(self, bot, name):
        self.bot = bot
        self.name = name
        self.orders = []
        self.location = None

        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()

    def turn(self, current):
        if self.orders:
            if not self.location:
                self.location = self.bot.location()
            else:
                self.bot.cannon(self.calculateAngle(self.orders.pop()),
                                self.calculateDistance(self.orders.pop()))

            self.bot.cannon(self.calculateAngle(self.orders.pop()),
                            self.calculateDistance(self.orders.pop()))
        else:
            self.location = self.bot.location()

        print("Turn of {} at location {},{}".format(
            id(self), self.location.x, self.location.y))
        sys.stdout.flush()

    def robotDestroyed(self, current):
        print("robot destroyed")
        sys.stdout.flush()

    def receiveOrders(self, point, current):
        self.orders.append(point)

    def calculateDistance(self, point):
        return math.sqrt(math.pow((self.location.x - point.x), 2) +
                         math.pow((self.location.y - point.y), 2))
#       return euclidean distance to point

    def calculateAngle(self, point):
        vector = [point.x - self.location.x, point.y - self.location.y]

        angle = vector[0] / (math.sqrt(1 + math.pow(vector[0], 2)) + math.sqrt(math.pow(vector[1]), 2))
#       This angle is the shortest angle between the direction to the point and the east(0 degrees angle)
#       If the point is lower to the location, the angle will be 360 - angle

        if point.x < self.location.x:
            angle = 360 - angle

        return int(angle)
