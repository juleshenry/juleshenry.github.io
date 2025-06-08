#!/bin/bash
title="${1// /-}"  # Replace spaces with hyphens in the title
date=$(date +%Y-%m-%d)
filename="${date}-${title}.md"
touch "$filename"
header="---\nlayout: post\ntitle: \"$1\"\ndate: $(date +%Y-%m-%d)\n---\n\n"
echo -e $header > "$filename"