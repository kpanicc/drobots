#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-


import Ice
Ice.loadSlice('drobots.ice')
import drobots


class RobotControllerI(drobots.RobotController):
    def __init__(self, bot):
        self.bot = bot

    def turn(self, current):
        print(self.bot.location())

    def robotDestroyed(self, current):
        print("robot destroyed")