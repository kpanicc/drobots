// -*- mode:c++ -*-

module drobots {

  struct Point {
    int x;
    int y;
  };

  exception NoEnoughEnergy{};

  interface RobotBase {
    void drive(int angle, int speed) throws NoEnoughEnergy;
    short damage() throws NoEnoughEnergy;
    short speed() throws NoEnoughEnergy;
    Point location() throws NoEnoughEnergy;
    short energy() throws NoEnoughEnergy;
  };

  interface Attacker extends RobotBase {
    bool cannon(int angle, int distance) throws NoEnoughEnergy;
  };

  interface Defender extends RobotBase {
    int scan(int angle, int wide) throws NoEnoughEnergy;
  };

  interface Robot extends Attacker, Defender {};

  interface RobotController {
    void turn();
    void robotDestroyed();
  };

  interface DetectorController {
    void alert(Point pos, int enemies); //enemies should be robots, it also detects our own
  };

  interface Player {
    RobotController* makeController(Robot* bot);
    DetectorController* makeDetectorController();
    Point getMinePosition();
    void win();
    void lose();
    void gameAbort();
  };

  exception GameInProgress{};
  exception InvalidProxy{};
  exception InvalidName{
    string reason;
  };
  exception BadNumberOfPlayers{};

  interface Game {
    void login(Player* p, string nick)
      throws GameInProgress, InvalidProxy, InvalidName;
  };

  interface GameFactory {
    Game* makeGame(string gameName, int numPlayers)
      throws InvalidName, BadNumberOfPlayers;
  };

  interface RBFactory{
      RobotController* makeRobotController(string name, Robot* bot);
  }

  exception AlreadyExists { string key; };
  exception NoSuchKey { string key; };
  dictionary<string, RBFactory*> RBFactoryPrxDict;
  interface FactoryContainer {
      void link(string key, RBFactory* proxy) throws AlreadyExists;
      void unlink(string key) throws NoSuchKey;
      RBFactoryPrxDict list();
  };
  

};
