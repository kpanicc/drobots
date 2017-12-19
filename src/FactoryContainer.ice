// -*- mode:c++ -*-
#include <factories.ice>


module drobots {
    exception AlreadyExists { string key; };
    exception NoSuchKey { string key; };
    dictionary<string, RBFactory*> RBFactoryPrxDict;
    interface FactoryContainer {
        void link(string key, RBFactory* proxy) throws AlreadyExists;
        void unlink(string key) throws NoSuchKey;
        RBFactoryPrxDict list();
    };
};