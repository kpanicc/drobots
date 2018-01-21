import Ice.*;

public final class DetectorControllerFactoryI extends drobotscomm._ControllerFactoryDisp {
    
    private int count = 0;

    @Override
    public void resetCount() {
        count = 0;
        return;
    }

    @Override
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
        drobots.DetectorControllerPrx finalPrx = drobots.DetectorControllerPrxHelper.checkedCast(directPrx);
        System.out.println("Direct proxy casted");
        System.out.flush();

        ObjectPrx cPrx = current.adapter.getCommunicator().propertyToProxy("DetectorContainer");
        drobotscomm.DetectorContainerPrx containerPrx = drobots.DetectorContainerPrxHelper.checkedCast(cPrx);
        containerPrx.link("Detector" + this.count, finalPrx);
        System.out.println("Detector " + this.count + " linked to the container");

        this.count++;
        return finalPrx;
    }
}
