#!/usr/bin/env bash
{ time curl -X GET http://127.0.0.1:8020 > /dev/null 2>&1 ; } 2>> ./evaluation_scripts/results.txt