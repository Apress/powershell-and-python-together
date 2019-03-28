'''
PassList Test
'''

import sys

fileList = []
for eachLine in sys.stdin:
    entry = eachLine.strip()
    if entry:
        fileList.append(entry)

print fileList

