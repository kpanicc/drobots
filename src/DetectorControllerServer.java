import Ice.*;

import java.lang.Exception;
import java.util.Properties;

public class DetectorControllerServer extends Ice.Application {
    public int run(String[] args) {
        Ice.Communicator broker = null;
        try
        {
            broker = Ice.Util.initialize(args);

            Ice.Properties props = broker.getProperties();

            DetectorControllerI servant = new DetectorControllerI();
            ObjectAdapter adapter = broker.createObjectAdapter(props.getProperty("AdapterName"));
            System.out.println("Propiedad name:" + props.getProperty("Name"));
            System.out.println("Propiedad AdapterName:" + props.getProperty("AdapterName"));
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
        DetectorControllerServer app = new DetectorControllerServer();
        app.main("DetectorController", args);
    }
}