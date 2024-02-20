
import numpy as np
from datetime import timedelta
from django.utils import timezone


import os
# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatAp.settings")

# Import the necessary parts of Django
import django

# Initialize Django
django.setup()
from chat.models import ChatMessage, Thread, Q, SentimentAnalysisResult
from accounts.models import User


def query(current_user, other_user):
    thread = Thread.objects.filter(
        (Q(first_person=current_user, second_person=other_user) |
         Q(first_person=other_user, second_person=current_user))
    ).first()
    if thread:
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

        sent_res = SentimentAnalysisResult.objects.filter(
            Q(user=current_user, chat_message__thread=thread, chat_message__timestamp__gte=twenty_four_hours_ago) |
            Q(user=other_user, chat_message__thread=thread, chat_message__timestamp__gte=twenty_four_hours_ago)
        ).order_by('chat_message__timestamp')
        # print(sent_res)
        results_list = []
        results_set = set()
        for res in sent_res:
            result_key = res.chat_message.message
            if result_key not in results_set:
                user_name = res.user.username
                chat_message = res.chat_message.message
                sentiment = res.sentiment
                feedback = res.suggested_words
                #print(f"User: {user_name}, Message: {chat_message}, Sentiment: {sentiment}, Feedback: {feedback}")
                result = {
                    'user_name': user_name,
                    'chat_message': chat_message,
                    'sentiment': sentiment,
                    'suggested_words': feedback,
                }
                results_list.append(result)
                results_set.add(chat_message)
        return results_list

def convert_sent_to_2D(res):
    users = []
    sentiments = []

    for r in res:
        user_name = r['user_name']
        sentiment = r['sentiment']
        users.append(user_name)
        sentiments.append(sentiment)

    unique_users = np.unique(users)
    sentiments_list = [[sentiments[i] for i in range(len(users)) if users[i] == user] for user in unique_users]

    return sentiments_list,unique_users


all_users = User.objects.all()
current_user = all_users[4]
other_user = all_users[6]
# print(current_user,other_user)
res=query(current_user, other_user)
# print(res)
sentiments, users=convert_sent_to_2D(res)

