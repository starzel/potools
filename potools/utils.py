import polib
import re
import logging
log = logging.getLogger(__name__)

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
            log.error("There seems to be a duplicate Default entry for " \
                "msgid '%s'" % entry.msgid)
    else:
        log.debug("msgid '%s' in 'new' file does not have a default " \
            "translation." % entry.msgid)
        default = entry.msgid
    return default


def append_entry(pofile, entry, default_msgstr=None):
    """ """
    if default_msgstr is None:
        entry = polib.POEntry(
            msgid=entry.msgid,
            occurrences=entry.occurrences,
            comment=entry.comment
        )
    else:
        entry = polib.POEntry(
            msgid=entry.msgid,
            msgstr=default_msgstr.strip(),
            occurrences=entry.occurrences,
            comment=entry.comment
        )
    pofile.append(entry)
    return pofile


def msg_is_updated(msg):
    """Returns False is the message is empty or fuzzy"""
    if not msg.msgstr:
        return False
    if u'fuzzy' in msg.flags:
        return False
    return True
