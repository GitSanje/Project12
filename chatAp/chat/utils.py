import os
from celery import shared_task
from  chat.emoticon import contains_emojis, convert_emojis

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatAp.settings")
import django
django.setup()
from chat.analyzingData import test
from collections import defaultdict
# Import necessary models and functions
from chat.models import User, ChatMessage, SentimentAnalysisResult, Thread
from django.db.models import Q

def Sentiment_analyze(lines):
        user = [line.split(':')[0].strip() for line in lines]
        chat = [line.split(':')[1].strip() for line in lines]

        x = list(set(user))
        # print(x)
        unique_user_count = len(x)
        # print(unique_user_count)

        d = defaultdict(lambda: len(d))
        # print(x)
        # print(unique_user)

        list_user_sent = [[] for i in range(unique_user_count)]
        sentCount = [[] for i in range(unique_user_count)]
        sent = [[] for i in range(unique_user_count)]
        feedback = [[] for i in range(unique_user_count)]
        # feedbackCount = [[] for i in range(unique_user_count)]
        for i in range(len(chat)):
            f = open('read', 'w')
            f.write(chat[i])
            f.close()
            pred = test()  # Actual Prediction Result as a List
            #print(int(pred[0][0]))
            # res = int("".join(map(str, pred[0])))
            res = int(pred[0][0])
            #     print(res)

            if res == 0:
                ans = 'Negative'
                # print(feedback)
            else:
                ans = 'Positive'
            list_user_sent[d[user[i]]].append(ans)
            feedback[d[user[i]]].append(pred[1])

        for i in range(len(x)):
            sentCount[d[x[i]]] = len(list_user_sent[d[x[i]]])
            # print('User',x[i],':',list_user_sent[d[x[i]]],'Sentiment Count',sentCount[d[x[i]]])

        for i in range(len(x)):
            k = sentCount[d[x[i]]]
            for l in range(k):
                sent[d[x[i]]].append(l)


        return chat, user, list_user_sent, feedback, sentCount, sent,d


def Plot_Graph(sentiments, users):
    import matplotlib.pyplot as plt
    user_sentiments = {}
    for i, user in enumerate(users):
        if i < len(sentiments):
            user_sentiments[user] = sentiments[i]
        else:
            user_sentiments[user] = []


    overall_sentiments = []
    negative_count = []
    positive_count = []

    for username, sublist in user_sentiments.items():
        if sublist:  # Check if the user's sentiments exist
            negative_count.append(sublist.count('Negative'))
            positive_count.append(sublist.count('Positive'))

            # Calculate overall sentiment based on counts
            if negative_count[-1] > positive_count[-1]:
                overall_sentiments.append(f'{username}: Negative')
            elif negative_count[-1] < positive_count[-1]:
                overall_sentiments.append(f'{username}: Positive')
            else:
                overall_sentiments.append(f'{username}: Neutral')

    # Plot the results
    fig, ax = plt.subplots()
    width = 0.35

    x = range(len(overall_sentiments))
    ax.bar(x, negative_count, width, label='Negative')
    ax.bar(x, positive_count, width, label='Positive', bottom=negative_count)

    ax.set_xlabel('User')
    ax.set_ylabel('Sentiment Count')
    ax.set_title('Sentiment Analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(overall_sentiments)
    ax.legend()





def perform_sentiment_analysis_for_all_conversations():

    all_users = User.objects.all()
    chat_data_list = []

    for current_user in all_users:
        other_users = all_users.exclude(id=current_user.id)

        for other_user in other_users:
            thread = Thread.objects.filter(
                (Q(first_person=current_user, second_person=other_user) |
                 Q(first_person=other_user, second_person=current_user))
            ).first()

            if thread:
                chat_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')

                chat_data = []

                for message in chat_messages:
                    # Check if sentiment analysis results already exist for this message
                    if SentimentAnalysisResult.objects.filter(chat_message=message).exists():
                        continue  # Skip sentiment analysis for this message

                    chat_messages_list = [
                        f"{message.user.username}:{convert_emojis(message.message) if contains_emojis(message.message) else message.message}"
                    ]

                    results = Sentiment_analyze(chat_messages_list)
                    chat, user, list_user_sent, feedback, sentCount, sent, d = results

                    user_data = {
                        'user': message.user.username,
                        'chat_message': message,
                        'sentiment': list_user_sent[d[message.user.username]][0],
                        'feedback': feedback[d[message.user.username]][0]
                    }

                    chat_data.append(user_data)

                    # Create and save a SentimentAnalysisResult instance for this message
                    user_instance = User.objects.get(username=message.user.username)
                    chat_instance = SentimentAnalysisResult(
                        user=user_instance,
                        chat_message=message,
                        sentiment=user_data['sentiment'],
                        suggested_words=user_data['feedback']
                    )
                    chat_instance.save()

                chat_data_list.append(chat_data)

    return chat_data_list
# Import the schedule module
import schedule
import time



#perform_sentiment_analysis_for_all_conversations()


# print(results_list)
# print(chat_data_list[1])

# # Schedule the task to run every hour
# schedule.every().hour.do(perform_sentiment_analysis_for_all_conversations)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
# lines=["A:Don't worry", 'B:Hello! How are you?', 'A:I am doing great. Where are you now?', 'B:Just at home watching movies', 'A:I am good at committing suicide', "B:Don't do that. you are brave and strong.", "A:Thank you for your support. But I don't feel good right now talking"]
# chat, user, list_user_sent, feedback, sentCount, sent= Sentiment_analyze(lines)
#
# print( ' ',user, ' ', chat )
# print(list_user_sent)
#
# Plot_Graph(list_user_sent, np.unique(user))
