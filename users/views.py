from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import User


# Traditional way:
#
# def index(request):
#     latest_user_list = User.objects.order_by('-date_registered')[:5]
#     context = {
#         'latest_user_list': latest_user_list,
#     }
#     return render(request, 'users/index.html', context)
#
#
# def detail(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'users/detail.html', {'user': user})


# Generic views way:

class IndexView(generic.ListView):
    template_name = 'users/index.html'
    context_object_name = 'latest_user_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.order_by('-date_registered')[:5]


class DetailView(generic.DetailView):
    model = User
    template_name = 'users/detail.html'



def results(request, user_id):
    response = "You're looking at the results of user %s."
    return HttpResponse(response % user_id)
