// -*- mode:c++ -*-
#include <drobots.ice>

module drobots {
    interface RBFactory{
        RobotController* makeRobotController(string name, Robot* bot);
    }
}