#!/bin/bash

delete_cleaned_files() {
  local dir="$1"

  for entry in "$dir"/*; do
    if [ -d "$entry" ]; then      
      delete_cleaned_files "$entry"
    elif [[ "$entry" == *_cleaned_cleaned.txt ]]; then
      echo "Remove $entry"
      rm "$entry"
    fi
  done
}

delete_cleaned_files "data/output"
