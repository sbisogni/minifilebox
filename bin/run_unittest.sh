#!/bin/sh

pushd .
cd file_storage
coverage run -m unittest
coverage report -m
popd
