from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club, JoinRequest
from suite.forms import ClubJoinForm

# todo officer only
class HandleJoinRequest(LoginRequiredMixin, View):
  template_name = 'dashboard/handle_join_request.html'

  def get(self, request, club_id, *args, **kwargs):
    reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
    return render(request, self.template_name, { 'reqs' : reqs })

  def post(self, request, club_id, *args, **kwargs):
    req_id = request.POST['accept']
    if req_id:
      req = JoinRequest.objects.get(id=req_id)
      if req.cid.add_member(request.user, req.uid):
        # only process if sufficient permission
        req.delete()

    reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
    return render(request, self.template_name, { 'reqs' : reqs })

