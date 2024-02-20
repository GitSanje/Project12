from django.contrib import admin
from .models import Thread, ChatMessage, SentimentAnalysisResult
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

admin.site.register(ChatMessage)
admin.site.register(SentimentAnalysisResult)
class ChatMessage(admin.TabularInline):
    model = ChatMessage
class ThreadForm(forms.ModelForm):
    def clean(self):
        """
        This is the function that can be used to
        validate your model data from admin
        """
        super(ThreadForm, self).clean()
        first_person = self.cleaned_data.get('first_person')
        second_person = self.cleaned_data.get('second_person')

        lookup1 = Q(first_person=first_person) & Q(second_person=second_person)
        lookup2 = Q(first_person=second_person) & Q(second_person=first_person)
        lookup = Q(lookup1 | lookup2)
        qs = Thread.objects.filter(lookup)
        if qs.exists():
            raise ValidationError(f'Thread between {first_person} and {second_person} already exists.')
# Register your models here.
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
