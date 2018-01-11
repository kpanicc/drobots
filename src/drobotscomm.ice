// -*- mode:c++ -*-
#include <drobots.ice>

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

    dictionary<string, drobots::RobotController*> RobotDict;
    interface RobotContainer {
        void link(string key, drobots::RobotController* robot) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RobotDict list();
    };

    sequence<drobots::Point> points;
    interface GameObserver {
        points getrobots();
    };

};
