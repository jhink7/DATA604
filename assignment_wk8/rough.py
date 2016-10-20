import nltk
from nltk.corpus import gutenberg
import string
import pandas as pd
import matplotlib.pyplot as plt

table = string.maketrans("","")
def trans_punc(s):
    return s.translate(table, string.punctuation)

# Load in hamlet corpus
hammy_raw = gutenberg.words('shakespeare-hamlet.txt')

hammy_unique = set()
hammy_all_filtered = []
for w in hammy_raw:
    trans = trans_punc(str(w.lower()))
    # filter out empty strings
    if trans:
        hammy_unique.add(trans)
        hammy_all_filtered.append(trans)
print('Total Number of Words: %i' % len(hammy_all_filtered))

# set words to lowercase, remove punctuation

print('Number of Unique Words: %i' % len(hammy_unique))

fd = nltk.FreqDist([w.lower() for w in hammy_all_filtered])

# translate results into pandas dataframe
hammy_df = pd.DataFrame(fd.items(), columns=['Word', 'Frequency'])
hammy_df = hammy_df.sort(['Frequency'], ascending=[0])
hammy_df = hammy_df.head(200)

print hammy_df

# plot top 200 words frequency

fig, ax = plt.subplots(1, 1)
ax.get_xaxis().set_visible(False)   # Hide Ticks
hammy_df.plot.bar(table=False, ax=ax)
plt.savefig('words.png')

hammy_df['CummSum'] = hammy_df['Frequency'].cumsum()

hammy_df['GtHalf'] = hammy_df['CummSum'] > (len(hammy_all_filtered) / 2.0)

print hammy_df







