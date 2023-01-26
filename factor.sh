#!/bin/bash
# This script factorizes numbers given in a file
while IFS='' read -r line || [[ -n "$line" ]]; do
    factors=( $(factor $line) )
    printf "%s=%s*%s\n" "$line" "$(($line/${factors[1]}))" "${factors[1]}"
done < "$1"
