import Ice.*;

public final class DetectorControllerFactoryI extends drobotscomm._DetectorControllerFactoryDisp {
    
    @Override
    public drobots.DetectorControllerPrx makeDetectorController(Current current) {
        DetectorControllerI servant = new DetectorControllerI();
        System.out.println("Servant created");
        System.out.flush();
        ObjectPrx prx = current.adapter.addWithUUID(servant)
        System.out.println("Servant added");
        System.out.flush();
        ObjectPrx directPrx = current.adapter.createDirectProxy(prx.ice_getIdentity());
        System.out.println("Direct proxy created");
        System.out.flush();
        drobots.DetectorControllerPrx finalPrx = drobotscomm.DetectorControllerPrx.checkedCast(directPrx);
        System.out.println("Direct proxy casted");
        System.out.flush();

        return finalPrx;
    }
}