// -*- mode:c++ -*-
#include <drobots.ice>

module drobotscomm {
    interface RBFactory{
        drobots::RobotController* makeRobotController(string name, drobots::Robot* bot);
    };

    interface ControllerFactory{
        drobots::DetectorController* makeDetectorController();
        void resetCount();
    };

    interface RobotControllerSlave extends drobots::RobotController {
        drobots::Point getLocation();
    };


    dictionary<int, int> detections; //Relative time (increments of 0.2, number of detections
    interface SmartDetectorController extends drobots::DetectorController {
        drobots::Point getDetectorLocation();
        int getFirstDetectionTime();
        detections getDetectionHistory();
        detections getNewDetections(string name);
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

    dictionary<string, SmartDetectorController*> DetectorDict;
    interface DetectorContainer {
        void link(string key, SmartDetectorController* detector) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        DetectorDict list();
        void flush();
    };

    sequence<drobots::Point> points;
    interface GameObserver {
        points getrobots();
        void changeGameServer(string gameserver);
    };
};
