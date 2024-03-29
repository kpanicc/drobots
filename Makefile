#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(filter-out nodes/node3, $(basename $(shell ls nodes/node*.config | sort -r)))
NODE_DIRS=$(addprefix /tmp/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass
CLASSPATH=-cp ./build/classes:./build/generated:/usr/share/java/ice-3.6.4.jar

all: start-grid compile

compile: folders copyfiles drobots detectorcontroller detectorcontrollerfactory icepatchcalc

update: copyfiles icepatchcalc

%.class: src/%.java
	javac -d build/classes $(CLASSPATH) $< -Xdiags:verbose

folders:
	mkdir -p build
	mkdir -p build/generated
	mkdir -p build/classes

copyfiles:
	cp src/*.py build/
	cp src/*.ice build/
	
drobots: build/drobotscomm.ice build/drobots.ice
	slice2java -I./build --output-dir ./build/generated build/drobotscomm.ice
	slice2java -I./build --output-dir ./build/generated build/drobots.ice

detectorcontroller: SmartDetectorControllerI.class

detectorcontrollerfactory: DetectorControllerFactoryI.class DetectorControllerFactoryServer.class

icepatchcalc:
	icepatch2calc build/
	
start-script:
	./start.sh

stop-script:
	./stop.sh

start-grid: /tmp/db/registry $(NODE_DIRS) /tmp/db/Player
	icegridnode --Ice.Config=nodes/node1.config &

	@echo -- waiting registry to start...
	@while ! netstat -lptn 2> /dev/null | grep ":4061" > /dev/null; do \
	    sleep 1; \
	done

	@for node in $(filter-out nodes/node1, $(NODES)); do \
	    icegridnode --Ice.Config=$$node.config & \
	    echo -- $$node started; \
	done

	@echo -- ok

stop-grid:
	@for node in $(NODES); do \
	    $(IG_ADMIN) -e "node shutdown $$node"; \
	done

	@killall icegridnode
	@echo -- ok

show-nodes:
	$(IG_ADMIN) -e "node list"

/tmp/db/%:
	mkdir -p $(addprefix /tmp/db/,$(notdir $@))

clean: 
	-$(RM) *~
	-$(RM) -r ./build
