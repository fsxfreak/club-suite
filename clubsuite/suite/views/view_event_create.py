from django.http import HttpResponse
from django.views.generic import TemplateView

class EventCreate(TemplateView):
    template_name = 'event_create.html'


    def post(self, request, club_id):
      form = self.form_class(request.POST)
      club = get_object_or_404(Club, pk=club_id)
      if form.is_valid():
        event = form.save(club, commit=True)
