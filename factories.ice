// -*- mode:c++ -*-
#include drobots.ice

module factories {
    interface RB_Factory{
        RobotController* makeRobotController(string name, Robot* bot);
    }
}