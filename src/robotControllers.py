#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice("drobots.ice")
import drobots


class RobotControllerTotalI(drobots.RobotController):
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


class RobotControllerAttI(drobots.RobotController):
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