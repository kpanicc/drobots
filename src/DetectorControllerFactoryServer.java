import Ice.*;

import java.lang.Exception;
import java.util.Properties;

public class DetectorControllerFactoryServer extends Ice.Application {
    public int run(String[] args) {
        Ice.Communicator broker = communicator();
        try
        {
            Ice.Properties props = broker.getProperties();

            DetectorControllerFactoryI servant = new DetectorControllerI();
            ObjectAdapter adapter = broker.createObjectAdapter(props.getProperty("AdapterName"));
            ObjectPrx proxy = adapter.add(servant, broker.stringToIdentity(props.getProperty("Name")));

            System.out.println(proxy.toString());
            System.out.flush();

            adapter.activate();
            shutdownOnInterrupt();
            broker.waitForShutdown();
        } catch (Ice.LocalException e) {
            e.printStackTrace();
            return 1;
        } catch (Exception e) {
            System.err.println(e.getMessage());
            return 1;
        }

        return 0;
    }

    static public void main(String[] args) {
        DetectorControllerFactoryServer app = new DetectorControllerServer();
        for (String s : args) {
            System.out.println(s);
        }
        app.main("DetectorControllerFactory", args);
    }
}