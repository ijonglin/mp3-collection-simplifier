# Albumize
Some cars have such crappy MP3 players (Nissan Leaf 2015, ahem)
that both directories and number of files are limited.  So,
1000+ song collections are not supported unless we can group
the songs into a lot less files.  This script does just that
in a very destructive manner.  So, to use this script:

1. *ALWAYS* Make a copy of the MP3 thumb directory
1. Copy the Makefile, and albumize.py scripts into the top level
where the directory structure is two level {artist}/{album_name}/song.mp3
1. Run the command:
    ```bash
    make
    ```
1. The script will merge all albums that have more than one song
into a single merged mp3 ; for albums with only 1 song, the song
is moved into a single directory called one_offs.

## Example: Reduction factor

For my own music collection, the number of files and directories were reduced as follows:

| Type | Before Albumize | After Albumize |
|---|---|---|
| Number of Directories | 940 | 227 |
| Number of Files | 5847 | 601 |

2015 Nissan Leaf player requires <255 directories and <999 songs.
Of course, you no longer have the ability to forward between songs, but
at least it all fits on the thumbdrive.
