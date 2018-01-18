// -*- mode:c++ -*-
#include <drobots.ice>

module drobotscomm {
    interface RBFactory{
        drobots::RobotController* makeRobotController(string name, drobots::Robot* bot);
    };

    interface RobotControllerSlave extends drobots::RobotController {
        drobots::Point getLocation();
    };
	
	exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    dictionary<string, RBFactory*> RBFactoryPrxDict;
    interface FactoryContainer {
        void link(string key, RBFactory* proxy) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RBFactoryPrxDict list();
        void flush();
    };

    dictionary<string, RobotControllerSlave*> RobotDict;
    interface RobotContainer {
        void link(string key, RobotControllerSlave* robot) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RobotDict list();
        void flush();
    };

    sequence<drobots::Point> points;
    interface GameObserver {
        points getrobots();
        void changeGameServer(string gameserver);
    };
};
