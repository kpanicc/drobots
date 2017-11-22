#!/usr/bin/env python3
# -*- mode: python3; coding: utf-8 -*-

import Ice
Ice.loadSlice('drobots.ice')
import drobots


class DetectorControllerI(drobots.DetectorController):
    def alert(self, current, pos, enemies):
        pass
