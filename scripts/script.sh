#!/bin/bash

clean_text_file() {
  local dir="$1"

  for entry in "$dir"/*; do
    if [ -d "$entry" ]; then
      clean_text_file "$entry"
    elif [[ "$entry" == *.txt && "$entry" != *_cleaned.txt ]]; then
      echo "Cleaning $entry"
      python clean_text.py "$entry"
    fi
  done  
}

clean_text_file "data/output"
