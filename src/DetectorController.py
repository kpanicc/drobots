#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import Ice
import sys
Ice.loadSlice('drobots.ice')
import drobots


class DetectorControllerI(drobots.DetectorController):
    def alert(self, pos, enemies, current):
        print("Alert: {} robots detected at {},{}".format(
            enemies, pos.x, pos.y))
        sys.stdout.flush()
