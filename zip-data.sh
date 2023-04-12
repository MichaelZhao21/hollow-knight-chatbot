#!/bin/bash

if [ -d output-raw ]; then
    zip -r output-raw.zip output-raw
fi

if [ -d output-data ]; then
    zip -r output-data.zip output-data
fi

if [ -d output-kb ]; then
    zip -r output-kb.zip output-kb
fi