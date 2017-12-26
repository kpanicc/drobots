import Ice.*;


public final class DetectorControllerI extends drobots._DetectorControllerDisp {
    @Override
    public void alert(drobots.Point point, int enemies, Current __current) {
        System.out.println(point.toString() + "   " + enemies);
    }
}