import Ice.*;
import java.util.Map;
import java.util.HashMap;


public final class SmartDetectorControllerI extends drobotscomm._SmartDetectorControllerDisp {

    private double baseTime;
    private Map<Integer, Integer> detectionHistory;
    private Map<String, Integer> requestHistory;
    private final double timeIncrement = 0.1;
    private drobots.Point detectorLocation;
    private int firstDetectionTime;
    private int lastDetectionTime;

    public SmartDetectorControllerI() {
        System.out.println("Detector controller created");
        System.out.flush();
        this.baseTime = getUnixTime();
        this.detectionHistory = new HashMap<Integer, Integer>();
        this.requestHistory = new HashMap<String, Integer>();
        this.detectorLocation = null;
        this.firstDetectionTime = -1;
        this.lastDetectionTime = -1;
    }

    @Override
    public void alert(drobots.Point point, int enemies, Current __current) {
        if (this.detectorLocation == null) {
            this.detectorLocation = point;
        }
        if (this.firstDetectionTime < 0) {
            this.firstDetectionTime = getCurrentDiscretizedTime();
        }
        this.lastDetectionTime = getCurrentDiscretizedTime();

        detectionHistory.put(getCurrentDiscretizedTime(), enemies);

        System.out.println(point.x + "," + point.y + "   " + enemies);
    }

    @Override
    public final drobots.Point getDetectorLocation(Current __current) {
        return this.detectorLocation;
    }

    @Override
    public final int getFirstDetectionTime(Current __current) {
        return this.firstDetectionTime;
    }

    @Override
    public final Map<Integer, Integer> getDetectionHistory(Current __current) {
        return this.detectionHistory;
    }

    @Override
    public final Map<Integer, Integer> getNewDetections(String name, Current __current) {
        System.out.print(name + " asked for new detections");
        Map<Integer, Integer> returnValue = null;
        if (this.requestHistory.containsKey(name)) {
            returnValue = new HashMap<Integer, Integer>();

            int lastRequestTime = this.requestHistory.get(name);

            for (Integer key : this.detectionHistory.keySet()) {
                if (key > lastRequestTime) {
                    returnValue.put(key, this.detectionHistory.get(key));
                }
            }
            System.out.println("  and it did asked before for news, give only new detections.");
        } else {
            returnValue = getDetectionHistory();
            System.out.println("  and it did not asked before for news, create new entry in the dictionary.");
        }

        this.requestHistory.put(name, getCurrentDiscretizedTime());
        return returnValue;
    }

    @Override
    public final double getTimeIncrement(Current __current) {
        return this.timeIncrement;
    }

    private int getCurrentDiscretizedTime() {
        return discretizeTime(getUnixTime());
    }

    private int discretizeTime(double time) {
        return (int) Math.floor((time - this.baseTime) / this.timeIncrement);
    }

    private static double getUnixTime() {
        return System.currentTimeMillis() / 1000L;
    }
}
