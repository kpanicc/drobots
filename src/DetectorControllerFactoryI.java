import Ice.*;

public final class DetectorControllerFactoryI extends drobotscomm._ControllerFactoryDisp {
    
    private int count = 0;

    //@Override
    public void resetCount(Current __current) {
        count = 0;
        return;
    }

    //@Override
    public drobots.DetectorControllerPrx makeDetectorController(Current current) {
        SmartDetectorControllerI servant = new SmartDetectorControllerI();
        System.out.println("Servant created");
        System.out.flush();
        ObjectPrx prx = current.adapter.addWithUUID(servant);
        System.out.println("Servant added");
        System.out.flush();
        ObjectPrx directPrx = current.adapter.createDirectProxy(prx.ice_getIdentity());
        System.out.println("Direct proxy created");
        System.out.flush();
        drobotscomm.SmartDetectorControllerPrx finalPrx = drobotscomm.SmartDetectorControllerPrxHelper.checkedCast(directPrx);
        System.out.println("Direct proxy casted");
        System.out.flush();

        ObjectPrx cPrx = current.adapter.getCommunicator().propertyToProxy("DetectorContainer");
        drobotscomm.DetectorContainerPrx containerPrx = drobotscomm.DetectorContainerPrxHelper.checkedCast(cPrx);
        try {
            containerPrx.link("Detector" + this.count, finalPrx);
        } catch (drobotscomm.AlreadyExists ex) {
            System.err.println(ex.toString());
        }
        System.out.println("Detector " + this.count + " linked to the container");

        this.count++;
        return finalPrx;
    }
}
