#!/bin/bash

echo 'File name: '
read file

echo 'Commit message: '
read msg

echo 'Push commits? y/n'
read ans

git add $file && git commit -m "$msg"

if [ans == y]
then
    echo 'Pushing...'
    git push
fi