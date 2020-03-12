from textblob import TextBlob
# Text for Analysis
text = TextBlob('''

''')
# Autocorrect Feature
# text = text.correct()

adjectives = [] # Get all Adjectives in List
for item in text.tags:
    if item[1] == 'JJ' or item[1] == 'JJR' or item[1] == 'JJS':
        adjectives.append(item[0])

print(adjectives)
text.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])



for sentence in text.sentences:
    print(sentence.sentiment.polarity)
# 0.060
# -0.341

# blob.translate(to="es")  # 'La amenaza titular de The Blob...'
