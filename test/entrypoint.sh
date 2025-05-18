#!/bin/bash
# filepath: d:\Universidad\recursos\taurus api\test\entrypoint.sh

# Run the tests
bzt /tmp/test-v2.yaml -o module=artifacts-dir=/tmp/artifacts

bzt /tmp/test-v1.yaml -o module=artifacts-dir=/tmp/artifacts