# Word2Vec Games

A cross-platform app made with Kivy and Python, using Gensim's word2vec model of word meanings/relationships to automatically generate questions for word games. Currently uses the Google News word vectors dataset. 

Currently has three games: 
- Odd One Out. Two random words are chosen from within the dataset, and one of these has two related words found by the model. User scores a point if they select the word that is not related to the other three
- Word Maths. Inspired by the famous 'king - man + woman = queen' equation, the model again selects two random words and adds their vectors together, finding the closest words to the resulting vector. The user scores a point if they enter any of the top matches. The use of completely random words means this currently is very difficult or questions often do not match the intended spirit of the game
- Closest Pair. Four pairs of closesly or loosely related words are randomly generated and the user gets a point for selecting the pair that is most closely related.

The first time the app is run, there will likely be a significant delay before it starts, while the large dataset is downloaded.
