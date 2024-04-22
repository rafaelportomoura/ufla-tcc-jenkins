#!/bin/bash
version=1.87

java -jar "$(dirname $0)/job-dsl-core-${version}-jar-with-dependencies.jar" -j $@
