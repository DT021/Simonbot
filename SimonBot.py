import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import numpy as np
import random

num_words = 25000  # how many words to learn
tokenizer = Tokenizer(oov_token='si', num_words=num_words+1)
data = open('Conversations.txt').read()
corpus = data.lower().split("\n")

tokenizer.fit_on_texts(corpus)
tokenizer.word_index = {e: i for e, i in tokenizer.word_index.items() if i <= num_words}  # tokenizer is 1 indexed
tokenizer.word_index[tokenizer.oov_token] = num_words + 1

total_words = len(tokenizer.word_index) + 3
print(tokenizer.word_index)
print(total_words)

input_sequences = []
# This part takes sequences of 2-10 words and uses them for training to predict the next word
for index in range(len(corpus)//100):
    for line in corpus[index*10:(index+1)*10]:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)

# pad sequences
max_sequence_len = max([len(x) for x in input_sequences])
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

# create predictors and label (in this case there might be more labels than words used
xs, labels = input_sequences[:, :-1], input_sequences[:, -1]
ys = tf.keras.utils.to_categorical(labels, num_classes=total_words)

start_from_scratch = False  # choose to make a new model or train an existing one

if start_from_scratch:
    model = Sequential()
    model.add(Embedding(total_words, 100, input_length=max_sequence_len-1))
    model.add(Bidirectional(LSTM(150)))
    model.add(Dense(total_words, activation='softmax'))
else:
    model = tf.keras.models.load_model("SimonBotModel.h5")

adam = Adam(lr=0.01)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
history = model.fit(xs, ys, epochs=2, verbose=1)
print(model.summary())

model.save("SimonBotModel.h5")

seed_text = "Hello, what's Up?\n"   # Start text
next_words = 5 + round(10*random.random())

for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed_text])[0]
    token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
    predicted = model.predict_classes(token_list, verbose=0)
    output_word = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output_word = word
            break
    seed_text += " " + output_word
print(seed_text)
