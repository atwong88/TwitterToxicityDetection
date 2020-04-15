import numpy as np
import pandas as pd
import utils

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from tensorflow.python.keras.models import Model
from tensorflow.python.keras.layers import Input, Dense, Embedding, SpatialDropout1D, Dropout, concatenate
from tensorflow.python.keras.layers import GRU, LSTM, Bidirectional, GlobalAveragePooling1D, GlobalMaxPooling1D
from tensorflow.python.keras.preprocessing import text, sequence
from tensorflow.python.keras.callbacks import Callback, ModelCheckpoint

class RocAucEvaluation(Callback):
    def __init__(self, validation_data=(), interval=1):
        super(Callback, self).__init__()

        self.interval = interval
        self.X_val, self.y_val = validation_data

    def on_epoch_end(self, epoch, logs={}):
        if epoch % self.interval == 0:
            y_pred = self.model.predict(self.X_val, verbose=0)
            score = roc_auc_score(self.y_val, y_pred)
            print("\n ROC-AUC - epoch: %d - score: %.6f \n" % (epoch+1, score))

def get_model(max_features=30000, embed_size=300):
    inp = Input(shape=(maxlen, ))
    x = Embedding(max_features, embed_size, weights=[embedding_matrix])(inp)
    x = SpatialDropout1D(0.2)(x)
    x = GRU(80, return_sequences=True)(x)
    avg_pool = GlobalAveragePooling1D()(x)
    max_pool = GlobalMaxPooling1D()(x)
    conc = concatenate([avg_pool, max_pool])
    outp = Dense(1, activation="sigmoid")(conc)
    
    model = Model(inputs=inp, outputs=outp)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model

max_features = 30000
embed_size = 300

# pre-trained embedding file
#embedding_file = 'embeddings/crawl-300d-2M.vec'
embedding_file = 'embeddings/glove.840B.300d.txt'

X_train, y_train, X_test = utils.load_wiki_data()
twitter_df, twitter_text, twitter_y = utils.load_twitter_data()

# Tokenize data, takes about a minute
print('Tokenizing data ...')
maxlen=100
tokenizer = utils.initialize_tokenizer(list(X_train)+list(X_test)+list(twitter_text))
x_train = sequence.pad_sequences(tokenizer.texts_to_sequences(X_train), maxlen=maxlen)
x_test = sequence.pad_sequences(tokenizer.texts_to_sequences(X_test), maxlen=maxlen)
twitter_tokenized = sequence.pad_sequences(tokenizer.texts_to_sequences(twitter_text), maxlen=maxlen)
print('Tokenizing completed.')

# Compute embedding matrix, takes 3 minutes
print('Computing embedding matrix ...')
def get_coefs(word, *arr): return word, np.asarray(arr, dtype='float32')
embeddings_index = dict(get_coefs(*o.rstrip().rsplit(' ')) for o in open(embedding_file, encoding='utf-8'))

word_index = tokenizer.word_index
nb_words = min(max_features, len(word_index))
embedding_matrix = np.zeros((nb_words, embed_size))

for word, i in word_index.items():
    if i >= max_features: continue
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None: embedding_matrix[i] = embedding_vector
print('Done.')

# initialize model
model = get_model()

#train model
batch_size = 32
epochs = 3
X_tra, X_val, y_tra, y_val = train_test_split(x_train, y_train, train_size=0.95, random_state=233)
RocAuc = RocAucEvaluation(validation_data=(X_val, y_val), interval=1)

# checkpoint
filepath="best_model_checkpoint.h5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=0, save_best_only=True, mode='max', save_freq='epoch')

hist = model.fit(X_tra, y_tra, batch_size=batch_size, epochs=3, validation_data=(X_val, y_val), callbacks=[RocAuc, checkpoint], verbose=1)