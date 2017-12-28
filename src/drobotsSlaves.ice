// -*- mode:c++ -*-
#include <drobots.ice>

module drobotsSlaves{
    interface robotControllerAttackerSlave extends drobots::RobotController{
        void receiveOrders(drobots::Point point);
    }
}