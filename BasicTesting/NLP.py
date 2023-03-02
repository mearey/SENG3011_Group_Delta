import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize;

print(sent_tokenize("Tokenizing by word: Words are like the atoms of natural language. They’re the smallest unit of meaning that still makes sense on its own. Tokenizing your text by word allows you to identify words that come up particularly often. For example, if you were analyzing a group of job ads, then you might find", "english"));