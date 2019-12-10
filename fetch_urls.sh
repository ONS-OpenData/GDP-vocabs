#!/bin/bash

while read url; do
    curl -sfLH 'Accept: text/turtle' "$url" || true
done
