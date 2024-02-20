from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.dashboard import dashboard_counts
@login_required(login_url='login')
def Dashboard(request):
    pos,neg = dashboard_counts(request.user.id)
    context = {
        'pos':pos,
        'neg':neg
    }
    print(request.user.id,pos,neg)
    return render(request, 'dashboard.html', context=context)
