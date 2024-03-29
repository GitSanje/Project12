

def test():
    import pandas as pd
    import joblib,os
    import re
    import matplotlib.pyplot as plt
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.corpus import wordnet as wn
    plt.style.use('ggplot')

    def sentiment_analyze(sentiment_prediction):
        neu = 0
        neg = sentiment_prediction.count(0)
        pos = sentiment_prediction.count(1)
        print('Neg:', neg, ', Pos:', pos)
        if neg > pos:
            print('Feedback: Negative')
            # SpeakText('Feedback is Negative')
        elif pos > neg:
            print('Feedback: Positive')
            # SpeakText('Feedback is Positive')
        else:
            neu += 1
            print('Feedback: Neutral')
            # SpeakText('Feedback is Neutral')
        #feedbackGraph(pos, neu, neg)

    def feedbackGraph(pos, neu, neg):
        fig, ax1 = plt.subplots()
        feedback = ['positive', 'neutral', 'negative']
        ax1.bar(feedback, [pos, neu, neg])
        fig.autofmt_xdate()
        plt.savefig('feedback_graph.png')
        plt.show()

    #print('================Loading the Model================')
    file_path = os.path.join(os.path.dirname(__file__), 'svm.pkl')

    # Define the file path to 'svm.pkl' in the same directory as your script

    model = joblib.load(file_path)
    #print('\n*****Ready*****')
    words = set(stopwords.words('english'))
    test_data = open('read', encoding='utf-8').read()
    #print(test_data)
    test_data = test_data.lower()
    wl = WordNetLemmatizer()
    text = " ".join([wl.lemmatize(i) for i in re.sub("[^a-zA-Z]", " ", test_data).split() if i not in words]).lower()
    #print(text)
    final_words = []
    final_words_copy = []
    final_words.append(text)
    for i in text.split():
        final_words_copy.append(i)
    vectorizer = model.named_steps['vect']
    text_vector = vectorizer.transform(
        final_words)  # Not actual use as vectorization is done internally. Used for creating dataframe for finding scores
    final_input_text = pd.DataFrame(text_vector.toarray(),
                                    columns=vectorizer.get_feature_names_out())  # Dataframe used just for finding scores

    # Prediction
    prediction = model.predict(final_words)
    prediction = prediction.tolist()  # Numpy Array to List

    # Uncomment the next line to display graphs
    #print(prediction)
    #sentiment_analyze(prediction)


    # finding score of word to give suggestions
    def findScore(w):
        return final_input_text[w].tolist()

    if prediction[0] == 1:
        return prediction, ""
    else:
        suggestions = []
        for w in final_words_copy:
            #if findScore(w)[0] > 0.4:
            if w in final_input_text.columns and findScore(w)[0] > 0.4:# Result of findScore(w) is a list hence [0] is used to retreive 1st element
                for syn in wn.synsets(w):
                    for l in syn.lemmas():
                        if l.antonyms():
                            suggestions.append(l.antonyms()[0].name())

        suggestions = list(set(suggestions))
        return prediction, suggestions
    # Plot the feedback graph


# uncomment the line below and run this file to analyze any text. Just need to write text read file.
# test()
