#!/bin/sh

pushd .
cd tests
python integration_test.py
popd

