#!/bin/bash


git add .

current_date=$(date +"%Y/%m/%d-%H:%M:%S")

git commit -m "Version-$current_date"

git push origin main
