import logging
import os
import polib
import re
import sys

VERBOSE = False
HELP = False

def loglevel():
    """Return DEBUG when -v is specified, INFO otherwise"""
    if VERBOSE:
        return logging.DEBUG
    return logging.INFO

logging.basicConfig(
            level=loglevel(),
            format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def get_package_root(dir=None):
    if dir is None:
        dir = os.getcwd()
    while 'setup.py' not in os.listdir(dir):
        newdir = os.path.dirname(dir)
        if newdir == dir:
            log.critical("Couldn't find python package root.")
            return 
        dir = newdir
    return dir
        

def usage(stream, func, msg=None):
    if msg:
        print >> stream, msg
        print >> stream
    program = os.path.basename(sys.argv[0])
    print >> stream, func.__doc__ % {"program": program}
    sys.exit(0)


def get_default(entry):
    """ Extract the default translation from the entry (without "Default:")
    """
    patt = re.compile("""Default:.?["\' ](.*?)(["\']$|$)""", re.S)
    match = patt.match(entry.comment)
    # Write the "Default: " text into the msgstr. Reason: Many translators will
    # not see comments in their translation program.
    default = entry.msgid
    if match:
        default = match.group(1).replace('\n', ' ')
        if "Default:" in default:
            print "ERROR! There seems to be a duplicate Default entry for " \
                "msgid '%s'" % entry.msgid
    else:
        print "WARNING! msgid '%s' in 'new' file does not have a default " \
            "translation." % entry.msgid
        default = entry.msgid
    return default

def append_entry(pofile, entry, default):
    """ """
    pofile.append(
        polib.POEntry(
                    msgid=entry.msgid,
                    msgstr=default.strip(),
                    occurrences=entry.occurrences,
                    comment=entry.comment)
                )
    return pofile

