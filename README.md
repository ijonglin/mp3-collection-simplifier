# mp3-collection-simplifier

## Overview
Some cars like the Nissan Leaf have some strange requirements on the MP3 collections.  Although there's no
limit on the size of the USB sticks, they may have some strange requirements such as:

* No support for unicode filenames
* No support beyond vanilla MP3 encoding

In any extra optional step, this project also reduces some filesystem requirements:

* Number of files
* Number of directories
* Number of files per directory

## Scripting

This project has a python script that non-destructively takes a huge album connection and:

1. Converts them into standard mp3 encoding (when necessary) with fun parallel script runner 
(5847 mixed mp3/AAC collection converted in <10 minutes on a Ryzen 7 system)
1. Attempts to clean up unicode weird character in the filenames
1. (in an optional step) Reduces the file count and number of directories by
group multiple songs into single Album files.

## Future

Currently, the scripts are hard-coded to my personal directory names.
However, if someone really asks, I can parametrized the scripts to
handle arbitrary directories.  Feel free to add an issue to this repo.

