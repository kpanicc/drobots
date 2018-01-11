// -*- mode:c++ -*-
//#include <drobots.ice>
#include <drobotsSlaves.ice>

module drobotscomm {
    interface RBFactory{
        drobots::RobotController* makeRobotController(string name, drobots::Robot* bot);
    };
	
	exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    dictionary<string, RBFactory*> RBFactoryPrxDict;
    interface FactoryContainer {
        void link(string key, RBFactory* proxy) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RBFactoryPrxDict list();
    };
    dictionary<string, drobotsSlaves::robotControllerAttackerSlave*> AttRobotDict;
    interface AttRobotContainer {
        void link(string key, drobotsSlaves::robotControllerAttackerSlave* robot) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        AttRobotDict list();
    };

    sequence<drobots::Point> points;
    interface GameObserver {
        points getrobots();
    };

};
