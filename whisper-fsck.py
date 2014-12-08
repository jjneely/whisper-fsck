import os
import sys
import os.path
import time
import optparse

sys.path.append("/opt/graphite/lib")

import whisper

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def fsck(path, fix=False):
    try:
        info = whisper.info(path)
    except whisper.CorruptWhisperFile as e:
        print "Found: %s" % str(e)
        badname = path + ".corrupt.%s" % time.strftime("%Y%m%d-%H%M%S")
        if fix:
            print "Moving %s => %s" % (path, badname)
            os.rename(path, badname)
        return 1
    except Exception as e:
        print "ERROR (unhandled): %s" % str(e)
        return 1

    return 0

def main():
    description = """Search for .WSP files under the given directory, or /opt/graphite/storage/whisper by default, for any Whisper database files that cannot be opened and read.  Optionally move those files out of the way."""
    usage = "usage: %prog [--fix|-f] [directory]"
    parse = optparse.OptionParser(description=description, usage=usage)
    parse.add_option("-f", "--fix",
                     action="store_true",
                     dest="fix",
                     default=False,
                     help="Move corrupt files out of the way.")

    opts, args = parse.parse_args()

    print "Graphite Whisper FSCK"
    print "Written by Jack Neely <jjneely@42lines.net>"
    print

    if len(args) > 1:
        storage = args[1]
    else:
        storage = "/opt/graphite/storage/whisper"

    spinner = spinning_cursor()
    c = 0
    errors = 0
    sys.stdout.write("Scanning %s..." % storage)
    for dirpath, dirnames, filenames in os.walk(storage):
        sys.stdout.write(spinner.next())
        sys.stdout.flush()
        for i in filenames:
            if i.endswith(".wsp"):
                c += 1
                errors += fsck(os.path.join(dirpath, i), opts.fix)
        sys.stdout.write('\b')

    sys.stdout.write('\n')
    print "%s whisper files examined." % c
    print "%s errors." % errors

    print "Done!"

if __name__ == "__main__":
    main()
