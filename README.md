# Whisper FSCK

This python script aims to be useful in Graphite clusters to find and deal
with corrupt Whisper DB files.

It can be difficult to fix Whisper files and in many cases the corruption
is just a zero byte file.  This tool doesn't attempt to fix the Whisper
DB files, but it does move them out of the way of carbon-cache by
appending a string similar to the following to the file name:

    .corrupt.<YEAR><MONTH><DAY>-<HOUR><MINUTE><SECOND>

## Requirements

This script will need to import your Whisper python library.  So make
sure its installed somewhere in Python's path or in /opt/graphite/lib.

## Usage

If your Graphite storage directory can be found in the default location
then usage is very simple

    $ python fsck.py
    Graphite Whisper FSCK
    Written by Jack Neely <jjneely@42lines.net>
    
    Scanning /opt/graphite/storage/whisper...
    503958 whisper files examined.
    0 errors.
    Done!

Supply a directory if your storage directory is in a different
location:

    $ python fsck.py /data/whisper

Use the `-f` option to move corrupt files out of the way, otherwise
the script will just report.
