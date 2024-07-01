import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from test_articles import *

from reportlab.pdfgen.canvas import Canvas

seq_len = 1024
number_of_words = 5000


def nn_model(data_frame):
    neural_model = tf.keras.Sequential([
        tf.keras.layers.Embedding(number_of_words, 128, input_length=seq_len),
        tf.keras.layers.Conv1D(128, 5, activation='relu'),
        tf.keras.layers.MaxPooling1D(pool_size=2),
        tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(len(data_frame['label'].unique()), activation='softmax')
    ])

    neural_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0025),
                         loss='sparse_categorical_crossentropy',
                         metrics=['accuracy'])

    return neural_model


canvas = Canvas('NN models with rodo.pdf')

df = pd.read_csv("articles.csv")

label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

X_train, X_test, y_train, y_test = train_test_split(df['content'],
                                                    df['label'],
                                                    test_size=0.2,
                                                    random_state=42)

tokenizer = Tokenizer(num_words=number_of_words)
tokenizer.fit_on_texts(X_train)

X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

X_train_padded = pad_sequences(X_train_seq, maxlen=seq_len)
X_test_padded = pad_sequences(X_test_seq, maxlen=seq_len)

model = nn_model(df)
model.fit(X_train_padded,
          y_train,
          epochs=8,
          validation_split=0.2,
          batch_size=32)


loss, accuracy = model.evaluate(X_test_padded, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

y_pred = model.predict(X_test_padded)
y_pred_labels = y_pred.argmax(axis=1)

print("Accuracy:", accuracy_score(y_test, y_pred_labels))
print("Classification Report:\n", classification_report(y_test, y_pred_labels, target_names=label_encoder.classes_))

canvas.drawString(10, 10, "Model pelny, z nastepujacymi kategoriami:")
canvas.drawString(10, 30, str(set(df['label'].values.tolist())))
canvas.drawString(10, 50, f"Accuracy: {accuracy_score(y_test, y_pred_labels)}")
canvas.drawString(10, 70, '---------------------------------------')


def classify_new_article(article_content):
    seq = tokenizer.texts_to_sequences([article_content])
    padded = pad_sequences(seq, maxlen=seq_len)
    pred = model.predict(padded)
    label = pred.argmax(axis=1)[0]
    return label_encoder.inverse_transform([label])[0]


categories = ['historia-i-kultura',
              'kosmos', 'czlowiek',
              'zdrowie',
              'zycie',
              'technologia',
              'ziemia',
              'materia-i-energia']


for category in categories:
    predicted_section = classify_new_article(new_articles[category])
    print('ZGODA' if (predicted_section == category) else 'NIEPOPRAWNA KLASYFIKACJA',
          "Predicted Section:", predicted_section, "| Real section: ", category)

y_loc = 90


def make_raport(y, cat, accur):
    canvas.drawString(10, y, f"Model z wszystkimi kategoriami  bez {cat}):")
    canvas.drawString(10, y + 20, f"Accuracy: {accur}")
    canvas.drawString(10, y + 40, '--------------------------------------')


# model bez pojedynczych kategorii


for category in categories:

    df2 = df[~df['label'].isin([category])]

    # print(set(df2['label']))

    label_encoder = LabelEncoder()
    df2['label'] = label_encoder.fit_transform(df2['label'])

    X_train, X_test, y_train, y_test = train_test_split(df2['content'],
                                                        df2['label'],
                                                        test_size=0.2,
                                                        random_state=42)

    tokenizer = Tokenizer(num_words=number_of_words)
    tokenizer.fit_on_texts(X_train)

    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    X_train_padded = pad_sequences(X_train_seq, maxlen=seq_len)
    X_test_padded = pad_sequences(X_test_seq, maxlen=seq_len)

    model = nn_model(df2)

    model.fit(X_train_padded,
              y_train,
              epochs=8,
              validation_split=0.2,
              batch_size=32)

    loss, accuracy = model.evaluate(X_test_padded, y_test)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

    y_pred = model.predict(X_test_padded)
    y_pred_labels = y_pred.argmax(axis=1)

    acc = accuracy_score(y_test, y_pred_labels)

    # print("Accuracy:", acc)
    # print("Classification Report:\n", classification_report(y_test, y_pred_labels, target_names=label_encoder.classes_))

    make_raport(y_loc, category, acc)
    y_loc = y_loc + 60

canvas.save()
