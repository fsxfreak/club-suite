from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.urls import reverse

from suite.models import Club, JoinRequest
from suite.forms import ClubJoinForm

from guardian.shortcuts import get_perms
from django.core.exceptions import PermissionDenied

# todo officer only
class HandleJoinRequest(UserPassesTestMixin, LoginRequiredMixin, View):
  template_name = 'dashboard/handle_join_request.html'

  def test_func(self):
    club = get_object_or_404(Club, pk=self.kwargs['club_id'])
    if 'can_handle_join_requests' not in get_perms(self.request.user, club):
      raise PermissionDenied

    return True

  def get(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)
    reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
    return render(request, self.template_name, { 'reqs' : reqs, 'club' : club })

  def post(self, request, club_id, *args, **kwargs):
    club = Club.objects.get(pk=club_id)
    if 'accept' in request.POST:
         req_id = request.POST['accept']
         req = JoinRequest.objects.get(id=req_id)
         if req.cid.add_member(request.user, req.uid):
           # only process if sufficient permission
           req.delete()
    if 'delete' in request.POST:
         req_idDelete = request.POST['delete']
         req = JoinRequest.objects.get(id=req_idDelete)
         req.cid.remove_member(request.user, req.uid)
         req.delete()

    reqs = Club.objects.get(pk=club_id).joinrequest_set.all()
    return render(request, self.template_name, { 'reqs' : reqs, 'club' : club })
