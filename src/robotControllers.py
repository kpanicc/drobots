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
        self.firstTurn = True
        self.moveCounter = -1
        self.moving = False
        self.direction = -500
        self.damage = 0

        print("Created RobotController {}, for bot {}".format(name, repr(bot)))
        sys.stdout.flush()
        
    def getcontainers(self, broker):
        if self.robotcontainer is None:
            containerprx = broker.propertyToProxy("Container")
            self.robotcontainer = drobotscomm.RobotContainerPrx.checkedCast(containerprx)
            print("Robot Container obtained")
            sys.stdout.flush()
        if self.gameobserverprx is None:
            self.gameobserverprx = broker.propertyToProxy("GameObserver")
            self.gameobserverprx = drobotscomm.GameObserverPrx.checkedCast(self.gameobserverprx)
            print("Game Observer obtained")
            sys.stdout.flush()    

    def getLocation(self, current):
        return self.location

    def turn(self, current):
        self.getcontainers(current.adapter.getCommunicator())
            
        if self.destroyed:
            return

        self.getActualLocation()  # This would get us only 1 shot per turn, do something more each turn
        self.getActualDamage()

        if self.moveCounter > 0:
            self.moveCounter -= 1

        if self.moveCounter == 0:
            self.bot.drive(0, 0)
            self.energy -= 1

        gamerobotspromise = self.gameobserverprx.begin_getrobots()

        ourobotslocation = self.robotcontainer.list()
        ourobotslocation = list(map(lambda x: x.getLocation(), ourobotslocation.values()))

        for ourRobotPos in ourobotslocation:
            if ourRobotPos.x != self.location.x and \
                    ourRobotPos.y != self.location.y:
                self.shouldMoveAway(ourRobotPos)

        gamerobots = self.gameobserverprx.end_getrobots(gamerobotspromise)  # AMD

        random.shuffle(gamerobots)

        if not self.firstTurn:
            for robotPos in gamerobots:
                companion = False
                for ourRobotPos in ourobotslocation:
                    companion = self.iscompanion(ourRobotPos, robotPos)  # If, atleast one of our robots could be us
                if not companion:  # (Not updated location, then do not shoot at him)
                    print("Attempting to shoot {} from {}, robot {}".format(
                        robotPos, self.location, self.name))
                    sys.stdout.flush()
                    if self.shouldMoveAway(robotPos):
                        self.moveAway(robotPos)
                    if self.canshoot():
                        self.shoot(robotPos)

        self.energy = 100

        if self.firstTurn:
            self.firstTurn = False
        print("Turn of {} at location {},{}".format(
            id(self), self.location.x, self.location.y))
        sys.stdout.flush()

    def iscompanion(self, ourRobotPos, robotPos):
        return ourRobotPos.x - 2 <= robotPos.x <= ourRobotPos.x + 2 and \
                ourRobotPos.y - 2 <= robotPos.y <= ourRobotPos.y + 2

    def getActualLocation(self):
        print("Bot {} asked for its location".format(self.bot))
        sys.stdout.flush()
        self.location = self.bot.location()
        self.energy -= 1

    def shouldMoveAway(self, otherPosition):
        return self.calculateDistance(otherPosition) < 80 and self.moveCounter <= 0  # missiles would hit 2 or more

    def moveAway(self, otherPosition):
        angle = self.calculateAngle(otherPosition)
        angle = (angle + 180) % 360  # calculate opposite angle
        speed = 100
        if self.canmove(speed):
            print("Moving away from {} with angle {}".format(otherPosition, angle))
            sys.stdout.flush()
            self.move(angle, speed)
            self.moveCounter = 10

    def canshoot(self):
        return self.energy >= 50

    def shoot(self, position):
        print("Bot {} shooting at {},{}".format(self.bot, position.x, position.y))
        sys.stdout.flush()
        self.bot.cannon(self.calculateAngle(position), self.calculateDistance(position))
        self.energy -= 50

    def canmove(self, speed):
        return (self.energy >= 60 and speed != 0) or (self.energy >= 1 and speed == 0)

    def move(self, angle, speed):
        self.bot.drive(angle, speed)
        self.energy -= 1 if speed == 0 else 60
        self.moving = speed != 0
        self.direction = -500 if speed == 0 else angle

    def getActualDamage(self):
        self.damage = self.bot.damage()
        self.energy -= 1

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
