from django.shortcuts import render,redirect, get_object_or_404
from .models import Thread, ChatMessage,User
from accounts.models import FriendRequest
from django.http import JsonResponse
from django.db.models import Q
from .Query import query, convert_sent_to_2D
from .utils import Sentiment_analyze, Plot_Graph
from matplotlib import pyplot as plt
from django.contrib import messages
import  numpy as np
from io import BytesIO
import base64
import  matplotlib
matplotlib.use('Agg')

def Chat(request):
    user = request.user
    threads = Thread.objects.by_user(user=user).prefetch_related('chatmessage_thread').order_by('timestamp')
    # print(threads,request.user)
    for thread in threads:
        # print(thread.second_person.username)
        # print(thread.first_person.username)
        # print(thread.first_person.profile.image.url)
        if thread.first_person== request.user:
               print(request.user,thread.second_person,thread.id)
        else:
            print(request.user,thread.first_person,thread.first_person.full_name)


    context = {
            'threads': threads,
            'user': user
        }


    return render(request, 'chat2.html', context)

def get_other_users_data(request):
        threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp') # Retrieve your threads data
        other_users = {}

        for thread in threads:
            if thread.first_person.id != request.user.id:
                other_users[thread.id] = {
                    'profile_image_url': thread.first_person.profile.image.url,
                    'full_name': thread.first_person.full_name
                }
            else:
                other_users[thread.id] = {
                    'profile_image_url': thread.second_person.profile.image.url,
                    'full_name': thread.second_person.full_name
                }
        request_user_data = {
            'profile_image_url': request.user.profile.image.url,
            'full_name': request.user.full_name
        }
        other_users['request_user'] = request_user_data
        return JsonResponse(other_users)


def chat_sentiment(request, other_user_id):
    current_user = request.user

    # Get the other user using their ID
    other_user = get_object_or_404(User, id=other_user_id)

    # Find the chat thread between the current user and the other user
    thread = Thread.objects.filter(
        (Q(first_person=current_user, second_person=other_user) |
         Q(first_person=other_user, second_person=current_user))
    ).first()

    if not thread:
        return render(request, 'chat_sentiments.html', {'error_message': 'No chat history found with this user.'})

    sentiment_results = query(current_user, other_user)

    sentiments, users = convert_sent_to_2D(sentiment_results)

    Plot_Graph(sentiments, users)

    # Save the graph to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the BytesIO object to base64 for embedding in HTML
    graph = base64.b64encode(buffer.read()).decode('utf-8')

    context = {'sentiment_results': sentiment_results, 'graph': graph}

    return render(request, 'chat_sentiments.html', context=context)





def addFriends(request):
    current_user = request.user
    all_users = User.objects.exclude(Q(id=current_user.id) | Q(is_superuser=True))
    friends = []
    for other_user in all_users:
        thread_exists = Thread.objects.by_user(user=current_user).filter(
            Q(first_person=current_user, second_person=other_user) |
            Q(first_person=other_user, second_person=current_user)
        ).exists()
        if thread_exists:
            friends.append(other_user)
    print(all_users,friends)
    context = {
        'all_users': all_users,
        'friends': friends,
    }
    return render(request, 'addFriends.html', context)


from .models import Thread


def other_user_profile(request, user_id):
    other_user = User.objects.get(pk=user_id)

    # Check if the current user and the other user are friends
    are_friends = Thread.objects.filter(
        Q(first_person=request.user, second_person=other_user) |
        Q(first_person=other_user, second_person=request.user)
    ).exists()

    friends_count = Thread.objects.filter(Q(first_person=other_user) | Q(second_person=other_user)).count()
    frequest = FriendRequest.objects.filter(from_user=request.user, to_user=other_user).first()


    context = {
        'other_user': other_user,
        'are_friends': are_friends,
        'friends_count':friends_count,
        'frequest':frequest,
    }
    return render(request, 'other_user_profile.html', context=context)

def send_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user
    )
    if created:
        messages.success(request, f'Friend request has been sent to {user.username}!')
    else:
        messages.info(request, f'A friend request to {user.username} already exists.')
    return redirect('other_user_profile', user_id=user_id)




def cancel_friend_request(request, user_id):
    user = get_object_or_404(User, id=user_id)


    frequest = FriendRequest.objects.filter(from_user=request.user, to_user=user).first()

    if frequest:
        frequest.delete()
        messages.success(request, f'Friend request to {user.username} has been canceled.')
    else:
        messages.info(request, f'There is no friend request to cancel to {user.username}.')

    return redirect('other_user_profile', user_id=user_id)


def accept_friend_request(request, user_id):
    from_user = get_object_or_404(User, id=user_id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    if frequest:
        user1 = frequest.to_user
        user2 = from_user
        print(user1,user2)
        Thread.objects.create(first_person=user1, second_person=user2)
        frequest.delete()
        messages.success(request, f'You are now friends with {from_user.username}.')
    else:
        messages.info(request, f'No friend request from {from_user.username} found.')
    return redirect('confirm_reject')

def reject_friend_request(request, user_id):
    from_user = get_object_or_404(User, id=user_id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    if frequest:
        frequest.delete()
        messages.success(request, f'You rejected to become friend with {from_user.username} .')
    else:
        messages.info(request, f'No friend request from {from_user.username} found.')
    return redirect('confirm_reject')


def accept_reject_request(request):

    all_requests = FriendRequest.objects.filter(to_user=request.user)
    print(all_requests)
    for req in all_requests:
        print(req.from_user)
    context = {
        'all_requests': all_requests
    }

    return render(request, 'confirm_reject.html', context=context)


