#!/bin/bash

FILE_PATH=$1
OUT_NAME=$(basename "${FILE_PATH%.*}")

mkdir -p "$OUT_NAME" out
ffmpeg -i $FILE_PATH -f image2 "$OUT_NAME"/%04d.png -y