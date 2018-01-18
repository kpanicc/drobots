// -*- mode:c++ -*-
#include <Ice/Identity.ice>

module drobots {
	interface Observable {
		void attach(Ice::Identity ident);
	};
	
	module GameObserver {
		struct BotInfo {
			int x;
			int y;
			string name;
			string color;
			int damage;		
		};
		sequence<BotInfo> BotSeq;
		
		struct MissileInfo {
			int x;
			int y;
			string id;
			string color;
			short angle;
		};
		sequence<MissileInfo> MissileSeq;
		
		struct ExplosionInfo {
			int x;
			int y;
			short hardRadius;
			short middleRadius;
			short softRadius;		
		};
		sequence<ExplosionInfo> ExplosionSeq;
		
		struct ScanInfo {
			int x;
			int y;
			short angle;
			short wide;
		};
		sequence<ScanInfo> ScanSeq;
		
		struct Snapshot {
			BotSeq bots;
			MissileSeq missiles;
			ExplosionSeq explosions;
			ScanSeq scans;
		};
		
		interface Canvas {
			void clean();
			void draw(Snapshot snapshot);
		};
	};
};
