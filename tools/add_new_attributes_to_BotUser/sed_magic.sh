# $1 = save file

sed -i.orig 's|"+4": "D83eDd8d", "+5": "D83dDd25", |"+3": "\\ud83e\\udd34", "+4": "\\ud83e\\udd8d", "+5": "\\ud83d\\udd25", |g' "$1"

# remember that in sed, backslashes need to be escaped => use double backslash
# there was a problem here: the \u wound up missing:
# sed -i.orig 's|"emoji_set": {|"emoji_set": {"+4": "\ud83e\udd8d", "+5": "\ud83d\udd25", |g' "$1"
