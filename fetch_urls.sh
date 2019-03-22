#!/bin/bash

while read url; do
    curl -LH 'Accept: text/turtle' "$url"
done
