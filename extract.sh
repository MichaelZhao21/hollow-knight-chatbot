#!/bin/bash

if [ -f output-raw.zip ]; then
    unzip -o output-raw.zip
fi

if [ -f output-data.zip ]; then
    unzip -o output-data.zip
fi

if [ -f output-kb.zip ]; then
    unzip -o output-kb.zip
fi
