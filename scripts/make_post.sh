#!/bin/bash
# Usage: scripts/make_post.sh "Title of the post"
set -euo pipefail
title="$1"
date=$(date +%Y-%m-%d)
# Spaces become hyphens; quotes and other URL-hostile characters are dropped
slug=$(printf '%s' "$title" | tr ' ' '-' | sed 's/[^[:alnum:]_.=-]//g')
escaped=$(printf '%s' "$title" | sed 's/["\\]/\\&/g')
filename="_posts/${date}-${slug}.md"
if [ -e "$filename" ]; then
  echo "$filename already exists" >&2
  exit 1
fi
cat > "$filename" <<EOF
---
layout: post
title: "${escaped}"
date: ${date}
description: ""
---

EOF
echo "$filename"
echo "When the title is final: node scripts/make_social_cards.mjs"
