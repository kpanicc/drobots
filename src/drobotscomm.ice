// -*- mode:c++ -*-

module drobotscomm {
    interface RBFactory{
        RobotController* makeRobotController(string name, Robot* bot);
    };
	
	exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    dictionary<string, RBFactory*> RBFactoryPrxDict;
    interface FactoryContainer {
        void link(string key, RBFactory* proxy) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RBFactoryPrxDict list();
    };

};