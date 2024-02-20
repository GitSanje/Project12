import logging
import os
from celery import shared_task
from  chat.emoticon import contains_emojis, convert_emojis

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Chat_ml.settings")
import django
django.setup()
from celery import shared_task
from chatAp.celery import  app
from celery.schedules import crontab
# from celery.decorators import periodic_task
from datetime import timedelta
from chat.models import User, ChatMessage, SentimentAnalysisResult, Thread
from django.db.models import Q
from chat.utils import Sentiment_analyze
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# app = Celery('Chat_ml',broker='pyamqp://0.0.0.0:5672',backend='rpc://')
#@periodic_task(run_every=crontab(minute=0, hour=0))
# @shared_task
# @app.task
# def run_sentiment_analysis_for_all_conversations():
#     logging.info("Starting sentiment analysis task...")
#     perform_sentiment_analysis_for_all_conversations()
#     logging.info("Sentiment analysis task completed.")

@shared_task
def perform_sentiment_analysis_for_all_conversations():
    start_time = datetime.now()
    logger.info(f"Task started at {start_time}")

    chat_data_list = []

    # Retrieve all users in one database query
    all_users = User.objects.all()

    for current_user in all_users:
        other_users = all_users.exclude(id=current_user.id)

        for other_user in other_users:
            thread = Thread.objects.filter(
                Q(first_person=current_user, second_person=other_user) |
                Q(first_person=other_user, second_person=current_user)
            ).first()

            if thread:
                # Optimize database queries by retrieving chat messages in a single query
                chat_messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')

                chat_data = []

                # Prepare the list of messages for sentiment analysis
                chat_messages_list = [
                    f"{message.user.username}:{convert_emojis(message.message) if contains_emojis(message.message) else message.message}"
                    for message in chat_messages
                    if not SentimentAnalysisResult.objects.filter(chat_message=message).exists()
                ]

                if chat_messages_list:
                    results = Sentiment_analyze(chat_messages_list)
                    chat, user, list_user_sent, feedback, sentCount, sent, d = results

                    for message in chat_messages:
                        if not SentimentAnalysisResult.objects.filter(chat_message=message).exists():
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

    end_time = datetime.now()
    execution_time = end_time - start_time
    logger.info(f"Task completed at {end_time}. Execution time: {execution_time}")

    return chat_data_list
