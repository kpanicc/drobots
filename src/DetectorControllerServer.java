import Ice.*;

import java.lang.Exception;

public class DetectorControllerServer extends Ice.Application {
    public int run(String[] args) {
        Ice.Communicator communicator = null;
        try
        {
            communicator = Ice.Util.initialize(args);

            Properties props = communicator.getProperties();

            DetectorControllerI servant = new DetectorControllerI();
            ObjectAdapter adapter = communicator.createObjectAdapter(props.getProperty("AdapterName"));
            ObjectPrx proxy = adapter.add(servant, communicator.stringToIdentity(props.getProperty("Name")));
            System.out.println(proxy.toString());
            System.out.flush();
            adapter.activate();
            shutdownOnInterrupt();
            communicator.waitForShutdown();
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