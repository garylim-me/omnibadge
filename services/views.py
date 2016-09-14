from django.views import generic

from .models import Service


class IndexView(generic.ListView):
    template_name = 'services/index.html'
    context_object_name = 'latest_service_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Service.objects.all()


class DetailView(generic.DetailView):
    model = Service
    template_name = 'services/detail.html'
