from django.db import models
from django.db.models import Q
from  accounts.models import User
from time import timezone
from datetime import timedelta
# Create your models here.
class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):

    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class SentimentAnalysisResult(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        chat_message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
        sentiment = models.CharField(max_length=10)
        suggested_words = models.TextField(blank=True)
        timestamp = models.DateTimeField(auto_now_add=True)

        @classmethod
        def get_latest_result(cls, user):
            now = timezone.now()
            # Calculate the timestamp for 24 hours ago
            twenty_four_hours_ago = now - timedelta(hours=24)

            # Get the latest result created within the last 24 hours
            latest_result = cls.objects.filter(user=user, timestamp__gte=twenty_four_hours_ago).last()
            return latest_result

        # def save(self, *args, **kwargs):
        #     # Retrieve the chat_message from the related ChatMessage instance
        #     if not self.chat_message:
        #         self.chat_message = self.chat_message.message
        #     super().save(*args, **kwargs)

        class Meta:
            verbose_name = "Sentiment Analysis Result"
            verbose_name_plural = "Sentiment Analysis Results"