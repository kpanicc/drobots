#!/usr/bin/make -f
# -*- mode:makefile -*-

CLASSPATH=-classpath runtime/ice-3.6.4.jar
MODULE=drobots

all: folders drobots DetectorControllerI.class DetectorControllerServer.class copypython icepatchcalc

%.class: src/%.java
	javac -d build/classes $(CLASSPATH) $< build/generated/drobots/*.java src/*.java

folders:
	mkdir build
	mkdir build/generated
	mkdir build/classes
	
drobots: interfaces/drobots.ice
	slice2java --output-dir ./build/generated $<

copypython:
	cp src/*.py build/

icepatchcalc:
	icepatch2calc build/
	
dist:
	mkdir dist

gen-dist: all dist
	cp -r *.class Example dist/
	icepatch2calc dist/

clean:
	$(RM) *.class proxy.out *~
	$(RM) -r Example
	$(RM) -r dist

run-server: Server.class
	java $(CLASSPATH) \
	    Server --Ice.Config=Server.config | tee proxy.out

run-client: Client.class
	java $(CLASSPATH) \
	    Client '$(shell head -1 proxy.out)'
