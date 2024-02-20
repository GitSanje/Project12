from django.urls import path, re_path
from . import views
from .views import get_other_users_data
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', views.Chat, name='chat'),
    path('get_other_users_data/', get_other_users_data, name='get_other_users_data'),
    path('chat_sentiments/<int:other_user_id>/', views.chat_sentiment, name='chat_sentiments'),
    path('add_friends/', views.addFriends, name='add_friends'),
    path('other_user_profile/<int:user_id>/', views.other_user_profile, name='other_user_profile'),

    path('friend_request_send/<int:user_id>/', views.send_friend_request, name='friend_request_send'),
    path('cancel_friend_request/<int:user_id>/', views.cancel_friend_request, name='cancel_friend_request'),
    path('accept_friend_request/<int:user_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/<int:user_id>/', views.reject_friend_request, name='reject_friend_request'),

    path('confirm_reject/', views.accept_reject_request, name='confirm_reject'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)