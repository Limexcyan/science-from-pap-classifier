import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from test_articles import *

# import pypdf
# import reportlab

from reportlab.pdfgen.canvas import Canvas

canvas = Canvas("raporty8i7kategorii.pdf")

df = pd.read_csv("articles_without_rodo.csv")

print("Model pełny, z nastepujacymi kategoriami:")
print(set(df['label'].values.tolist()))


X_train, X_test, y_train, y_test = train_test_split(df['content'],
                                                    df['label'],
                                                    test_size=0.2,
                                                    random_state=42)

# Wektoryzacja tekstu przy użyciu TF-IDF dla max_features większych od 10000 accuracy znacząco spada
vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# dla n_estimators > 1000 strasznie długo mieli
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

y_loc = 10
canvas.drawString(10, y_loc, "Model pelny, z nastepujacymi kategoriami:")
y_loc = y_loc + 20
canvas.drawString(10, y_loc, str(set(df['label'].values.tolist())))
y_loc = y_loc + 20
canvas.drawString(10, y_loc, f"Accuracy: {accuracy_score(y_test, y_pred)}")
y_loc = y_loc + 20


# klasyfikacja artykułów z zewnętrznych stron


def classify_new_article(article_content):
    vectorized_content = vectorizer.transform([article_content])
    return model.predict(vectorized_content)[0]


categories = ['historia-i-kultura',
              'kosmos',
              'czlowiek',
              'zdrowie',
              'zycie',
              'technologia',
              'ziemia',
              'materia-i-energia']


for category in categories:
    predicted_section = classify_new_article(new_articles[category])
    print("Predicted Section:", predicted_section, "| Real section: ", category)
    print('ZGODA' if (predicted_section == category) else 'NIEPOPRAWNA KLASYFIKACJA')

print("Trudności ze znalezieniem artykułów z kategorii materia i energia")

for article in [materia_article2, materia_article3, materia_article4, materia_article5]:
    predicted_section = classify_new_article(article)
    print("Predicted Section:", predicted_section, "| Real section: ", "materia_i_energia")
    print('ZGODA' if (predicted_section == "materia_i_energia") else 'NIEPOPRAWNA KLASYFIKACJA')


# modele bez jednej kategorii

for category in categories:

    y_loc = y_loc + 20

    df2 = pd.read_csv("articles.csv")
    df2 = df2[~df2['label'].isin([category])]

    print(f"Model z następującymi kategoriami (wszystkie bez {category}):")
    print(set(df2['label'].values.tolist()))

    X_train, X_test, y_train, y_test = train_test_split(df2['content'],
                                                        df2['label'],
                                                        test_size=0.2,
                                                        random_state=42)

    vectorizer = TfidfVectorizer(max_features=1000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)
    acc = accuracy_score(y_test, y_pred)

    print("Accuracy:", acc)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    canvas.drawString(10, y_loc, f"Model z nastepujacymi kategoriami (wszystkie bez {category}):")
    y_loc = y_loc + 20
    canvas.drawString(10, y_loc, str(set(df2['label'].values.tolist())))
    y_loc = y_loc + 20
    canvas.drawString(10, y_loc, f"Accuracy: {acc}")
    y_loc = y_loc + 20
    canvas.drawString(10, y_loc, '--------------------------------------')

canvas.save()


# modele bez dwu kategorii

canvas = Canvas("raporty6kategorii.pdf")
y_loc = 20

for category in categories:
    if category != 'technologia':
        df2 = df[~df['label'].isin(['technologia', category])]

        print(f"Model z następującymi kategoriami (wszystkie bez technologia i {category}):")
        print(set(df2['label'].values.tolist()))

        X_train, X_test, y_train, y_test = train_test_split(df2['content'],
                                                            df2['label'],
                                                            test_size=0.2,
                                                            random_state=42)

        vectorizer = TfidfVectorizer(max_features=1000)
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train_tfidf, y_train)

        y_pred = model.predict(X_test_tfidf)

        acc = accuracy_score(y_test, y_pred)

        # print("Accuracy:", acc)
        # print("Classification Report:\n", classification_report(y_test, y_pred))

        canvas.drawString(10,
                          y_loc,
                          f"Model z nastepujacymi kategoriami (wszystkie bez technologia i {category}):")

        y_loc = y_loc + 20
        canvas.drawString(10, y_loc, str(set(df2['label'].values.tolist())))
        y_loc = y_loc + 20
        canvas.drawString(10, y_loc, f"Accuracy: {acc}")
        y_loc = y_loc + 20

canvas.save()


# modele z tylko dwiema kategoriami

checked = []
for category in categories:
    canvas = Canvas(str("raporty" + str(category) + "-vs" + ".pdf"))
    for category2 in categories:
        if len({category, category2}) == 2:

            df_A = df[df['label'].isin([category])]
            df_B = df[df['label'].isin([category2])]

            df2 = pd.concat([df_A, df_B])

            # print(set(df2['label']))

            X_train, X_test, y_train, y_test = train_test_split(df2['content'],
                                                                df2['label'],
                                                                test_size=0.2,
                                                                random_state=42)

            vectorizer = TfidfVectorizer(max_features=1000)
            X_train_tfidf = vectorizer.fit_transform(X_train)
            X_test_tfidf = vectorizer.transform(X_test)

            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train_tfidf, y_train)

            y_pred = model.predict(X_test_tfidf)
            acc = accuracy_score(y_test, y_pred)

            # print("Accuracy:", acc)

            canvas.drawString(10, y_loc, f"Porownanie: {category} vs {category2}):")
            y_loc = y_loc + 20
            canvas.drawString(10, y_loc, f"Accuracy: {acc}")
            y_loc = y_loc + 20
            canvas.drawString(10, y_loc, str('----------------------------------'))
            y_loc = y_loc + 20
    canvas.save()
