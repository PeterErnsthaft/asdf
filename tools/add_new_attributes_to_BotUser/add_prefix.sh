PREFIX="${1}" # e.g.  '"emoji_set": {"-1": "\ud83e\udd15",'
OLD="$(cat $2)" # save file
echo "{${PREFIX} ${OLD:1}" > $2  # delete opening curly brace from old string, add prefix and new curly brace, write to save file

