import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np

tokenizer = Tokenizer()

data = open('Conversations.txt').read()

conversations = data.lower().split("\n\n\n")  #TODO Data generated needs to be separated by \n\n\n between conversations

tokenizer.fit_on_texts(conversations)
total_words = len(tokenizer.word_index) + 1

#print(tokenizer.word_index)
print(total_words)
maxlength = 0

for block in conversations:
    separated_lines = block.lower().split("\n")
    for line in separated_lines:
        maxlength = max(maxlength, len(line.split(" ")))
print(maxlength)

input_sequences = []
print(len(conversations))
for block in conversations[:2]:      #TODO instead of taking all 15, take: 2,3,4....15 for start
    conversation_block = []
    print(block)
    separated_lines = block.lower().split("\n")
    #print(len(separated_lines))
    for line in separated_lines:
        token_list = tokenizer.texts_to_sequences([line])
        token_list = list(pad_sequences(token_list, maxlen=maxlength - 1, padding='pre')[0])
        #print(line)
        #print(token_list)
        conversation_block.append(token_list)

    token_array = np.array(conversation_block)
    print(token_array)
