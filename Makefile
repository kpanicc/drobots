#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(basename $(shell ls nodes/node*.config | sort -r))
NODE_DIRS=$(addprefix /tmp/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass
CLASSPATH=-classpath /usr/share/java/ice-3.6.4.jar

compile: folders copyfiles drobots DetectorControllerI.class DetectorControllerServer.class icepatchcalc

%.class: src/%.java
	javac -d build/classes $(CLASSPATH) $< build/generated/drobots/*.java src/*.java

folders:
	mkdir -p build
	mkdir -p build/generated
	mkdir -p build/classes
	
drobots: build/drobots.ice
	slice2java --output-dir ./build/generated $<

copyfiles:
	cp src/*.py build/
	cp src/*.ice build/

icepatchcalc:
	icepatch2calc build/

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
	-$(RM) -r /tmp/db
	-$(RM) -r ./build
