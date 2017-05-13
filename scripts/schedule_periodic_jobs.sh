#!/bin/bash

while IFS='' read -r line || [[ -n "$line" ]]; do
    curl -g 'https://app.scrapinghub.com/api/v2/projects/190405/periodicjobs' \
         -H 'Accept-Encoding: gzip, deflate, br' \
         -H 'Content-Type: application/json;charset=UTF-8' \
         -H 'Accept: application/json, text/plain, */*' \
         -H 'X-Feature: master' \
         -H 'Connection: keep-alive' \
         -H 'DNT: 1' \
         -H 'Referer: https://app.scrapinghub.com/p/190405/periodic-jobs' \
         -H 'X-CSRFToken: {X-CSRFToken' \
         -H 'Cookie: {Cookie}' \
         --data-binary "$line" \
         --compressed
done < "$1"