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
        print("Robot destroyed, robot position: {},{}".format(self.location.x, self.location.y))
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
        self.detectorcontainer = None
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
        if self.detectorcontainer is None:
            self.detectorcontainer = broker.propertyToProxy("DetectorContainer")
            self.detectorcontainer = drobotscomm.DetectorContainerPrx.checkedCast(self.detectorcontainer)
            print("Detector container obtained")
            sys.stdout.flush()

    def getLocation(self, current):
        return self.location

    def turn(self, current):
        ourobotslocation = None
        self.getcontainers(current.adapter.getCommunicator())
            
        if self.destroyed:
            return

        # AMI begin logic, let it receive data, we do not need it right now
        gamerobotspromise = self.gameobserverprx.begin_getrobots()
        ourobotspromise = self.robotcontainer.begin_list()

        self.getActualLocation()  # This would get us only 1 shot per turn, do something more each turn
        self.getActualDamage()

        # Moving away from enemies stopping logic
        if self.moveCounter > 0:
            self.moveCounter -= 1

        if self.moveCounter == 0:
            self.move(0, 0)
            self.moveCounter = -1

        # Detector data handling
        print("Handling detectors")
        sys.stdout.flush()
        detectors = list(self.detectorcontainer.list().values())

        random.shuffle(detectors)
        for detector in detectors:
            print("Using detector: {}".format(detector))
            sys.stdout.flush()
            if self.canshoot():  # No point in waste resources when we cannot shoot
                break
            newdetected = detector.getNewDetections(self.name)
            if len(newdetected) > 0:  # If we have news
                print("Detector {}   has news for us".format(detector))
                sys.stdout.flush()
                detected = newdetected[newdetected.keys().sort[-1]]  # Get the last detection
                if ourobotslocation is None:
                    ourobotslocation = self.robotcontainer.end_list(ourobotspromise)
                    ourobotslocation = list(map(lambda x: x.getLocation(), ourobotslocation.values()))
                    print("We got the location of our robots")
                    sys.stdout.flush()

                detectorlocation = detector.getDetectorLocation()
                alliedinside = self.getRobotsInCircle(detectorlocation, 40, ourobotslocation)
                if len(alliedinside) == 0:  # Shoot directly to the detector, some damage will be dealt to enemies
                    print("No allies inside this detector")
                    sys.stdout.flush()
                    if self.canshoot():
                        self.shoot(detectorlocation)
                elif 0 < len(alliedinside) < detected:
                    print("Allies inside this detector, computing farthest point from them")
                    sys.stdout.flush()
                    farthestpoint = self.computeFarthestPointInCircle(detectorlocation, 40, alliedinside)
                    print("Farthest point: {}".format(farthestpoint))
                    sys.stdout.flush()
                    if self.canshoot():
                        self.shoot(farthestpoint)
        print("Exited detector logic")
        sys.stdout.flush()

        # Maybe the detectors had no news and we did not got the ourobots data, collect it now
        if ourobotslocation is None:
            ourobotslocation = self.robotcontainer.end_list(ourobotspromise)
            ourobotslocation = list(map(lambda x: x.getLocation(), ourobotslocation.values()))

        # Moving away from enemies logic
        for ourRobotPos in ourobotslocation:
            if ourRobotPos.x != self.location.x and ourRobotPos.y != self.location.y:
                if self.shouldMoveAway(ourRobotPos):
                    if self.canmove(100):
                        self.moveAway(ourRobotPos)

        gamerobots = self.gameobserverprx.end_getrobots(gamerobotspromise)

        random.shuffle(gamerobots)
        if not self.firstTurn:  # We do not know the position of our robots, do not shoot in case we shoot ourselves
            for robotPos in gamerobots:  # For every robot in the match
                companion = False
                for ourRobotPos in ourobotslocation:
                    companion = self.iscompanion(ourRobotPos, robotPos)  # If, atleast one of our robots could be us
                    if companion:
                        break
                if not companion:  # (Not updated location, then do not shoot at him)
                    print("Attempting to shoot {},{} from {},{}, robot {}".format(
                        robotPos.x, robotPos.y, self.location.x, self.location.y, self.name))
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
        return ourRobotPos.x -2 <= robotPos.x and ourRobotPos.x + 2 >= robotPos.x and \
            ourRobotPos.y -2 <= robotPos.y and ourRobotPos.y + 2 >= robotPos.y

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
        print("Robot destroyed, robot position: {},{}".format(self.location.x, self.location.y))
        sys.stdout.flush()

    def getRobotsInCircle(self, center, radius, robotList):
        retlist = []
        for robot in robotList:
            if math.sqrt((robot.x - center.x )**2 + (robot.y - center.y)**2) <= radius:
                retlist.append(robot)

        return retlist

    def computeFarthestPointInCircle(self, circle, radius, pointlist):
        if len(pointlist) == 0:
            return None

        oppositepoints = []
        for point in pointlist:
            oppositepoints.append(drobots.Point(circle.x - (point.x - circle.x), circle.y - (point.y - circle.y)))

        meanx = meany = None
        for point in pointlist:
            meanx += point.x
            meany += point.y
        meanpoint = drobots.Point(meanx / len(pointlist), meany / len(pointlist))

        return self.getClosestPointInCircle(circle, radius, meanpoint)

    def getClosestPointInCircle(self, circle, radius, point):
        vx = point.x - circle.x
        vy = point.y - circle.y
        magv = math.sqrt(vx**2 + vy**2)
        if magv == 0:  # point == circle
            return point
        else:
            ax = circle.x + ((vx / magv) * radius)
            ay = circle.y + ((vy / magv) * radius)
            return drobots.Point(ax, ay)

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
