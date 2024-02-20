from datetime import timedelta
from django.utils import timezone
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatAp.settings")
import django
django.setup()

from chat.models import ChatMessage, Thread,  SentimentAnalysisResult
from django.db.models import Q
from  accounts.models import User



def dashboard_counts(target_user_id):
    target_user = User.objects.get(id=target_user_id)

    # Find all threads involving the target user
    threads = Thread.objects.filter(Q(first_person=target_user) | Q(second_person=target_user))

    sentiments = []
    # Initialize sentiment counts
    positive_count = 0
    negative_count = 0

    # Define the time threshold (24 hours ago)
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)

    # Iterate over each thread
    for thread in threads:
        # Find all chat messages in the thread within the last 24 hours
        chat_messages = ChatMessage.objects.filter(thread=thread, timestamp__gte=twenty_four_hours_ago)

        # Iterate over each chat message
        for chat_message in chat_messages:
            # Find sentiment analysis result associated with the chat message
            sentiment_result = SentimentAnalysisResult.objects.filter(chat_message=chat_message).first()
            if sentiment_result:
                sentiments.append(sentiment_result.sentiment)
                if sentiment_result.sentiment == 'Positive':
                    positive_count += 1
                elif sentiment_result.sentiment == 'Negative':
                    negative_count += 1
    return positive_count,negative_count

# Print the sentiment counts
# print('Positive count:', positive_count)
# print('Negative count:', negative_count)
