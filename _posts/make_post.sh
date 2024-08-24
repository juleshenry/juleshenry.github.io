#!/bin/bash
date=$(date +%Y-%m-%d);filename="${date}-${1}.md";touch "$filename"; 
header="---\nlayout: post\ntitle: \"$1\"\ndate: $(date +%Y-%m-%d)\n---\n\n";echo -e $header > $filename;