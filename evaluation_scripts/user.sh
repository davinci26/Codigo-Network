#!/usr/bin/env bash
{ time curl -X POST http://35.206.132.245/test:8020> /dev/null 2>&1 ; } 2>> ./evaluation_scripts/results.txt