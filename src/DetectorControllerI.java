import drobots.*;
import Ice.Current;
public final class DetectorControllerI extends drobots._DetectorControllerDisp {
    public void alert(Point point, int enemies, Current __current) {
        System.out.println(point.toString() + "   " + enemies);
    }
}