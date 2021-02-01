"""
Finds word frequency in a text file.
Uses Counter.
"""
import sys
import re
from collections import Counter

# Default values
f = 'test.txt'
x = 10

# Read arguments
if len(sys.argv)<2:
    print('python wordfrequency_r.py <textfile>')
    print('Assuming using default text file named test.txt and top 10 words')
elif len(sys.argv)<3:
    f = sys.argv[1]
else:
    f = sys.argv[1]
    x = int(sys.argv[2])

try:
    document_text = open(f, 'r')
except:
    print('File cannot be found!')
    print('Exiting...')
    sys.exit(2)
    
text_string = document_text.read().lower()
match_pattern = re.findall(r'\b[a-z]{4,15}\b', text_string)
#print(match_pattern)
word_counts = Counter(match_pattern)
#print(word_counts)

print(f"Find the top {x} most common words.")
for word, count in word_counts.most_common(x):
    print(word,count)
