from django.db import models
from django.utils import timezone
from django.db.models import Q

from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, remove_perm, get_perms

from stdimage.models import StdImageField

from suite.models import User

class ClubManager(models.Manager):
  def qry_searchclubs(self, keyword):
    c=Club.objects.filter(
        Q(club_name__contains=keyword) |
         Q(club_description__contains=keyword)
        )
    r=c.filter(club_type='PUB')
    return r

  def qry_searchoneclub(self, cid_in):
    c=Club.objects.get(id=cid_in)
    return c


class Club(models.Model):
  club_name = models.CharField(max_length=50,unique=True)

  class Meta:
    permissions = (
         ('can_remove_member', 'Can remove member'),
         ('can_handle_join_requests', 'Can handle join requests'),
         ('can_handle_promotion_requests', 'Can handle promotion requests'),
         ('can_view_stats', 'Can view individual member stats'),
         ('can_create_event', 'Can create an event for this club'),
         ('can_add_receipt', 'Can add a receipt'),
         ('can_remove_receipt', 'Can remove a receipt'),
         ('can_access_attendance', 'Can access member attendance'),
         ('can_access_budget', 'Can access the budgets for this club'),
         ('can_create_budget', 'Can create a budget'),
         ('can_request_reimbursement', 'Can request for a reimbursement'),
         ('can_handle_reimbursement', 'Can handle reimbursement'),
         ('can_view_account_info', 'Can view member personal information'),
         )

  C_CHOICES = (
      ('PUB','Public'),
      ('PRI','Private')
      )
  club_type = models.CharField(max_length=3,choices=C_CHOICES,default='PUB')
  image = StdImageField(default="default.jpg",
      variations={'cropped': {'width': 1600, 'height': 400, 'crop': True}})
  first_seen = models.DateTimeField(editable=False, blank=True, null=True)
  last_seen = models.DateTimeField(blank=True, null=True)
  club_description = models.TextField()
  requests = models.ManyToManyField(
                  User,
                  through='JoinRequest',
                  related_name='JoinRequest'
                  )

  members = models.ManyToManyField(User)
  objects = ClubManager()

  def __str__(self):
    return self.club_name

  def summary(self):
    return self.club_description[:100]

  def update_group_names(self, new_club_name):
    owner_group = self.get_owner_group()
    officer_group = self.get_officer_group()
    member_group = self.get_member_group()

    owner_group.name = '%s_owners' % new_club_name
    officer_group.name = '%s_officers' % new_club_name
    member_group.name = '%s_members' % new_club_name
    
    owner_group.save()
    officer_group.save()
    member_group.save()

  def _get_owner_group_name(self):
    return '%s_owners' % self.club_name
  def _get_officer_group_name(self):
    return '%s_officers' % self.club_name
  def _get_member_group_name(self):
    return '%s_members' % self.club_name

  def _get_owner_group(self):
    return Group.objects.get(name=self._get_owner_group_name())
  def _get_officer_group(self):
    return Group.objects.get(name=self._get_officer_group_name())
  def _get_member_group(self):
    return Group.objects.get(name=self._get_member_group_name())

  def get_owners(self):
    return self._get_owner_group().user_set.all()
  def get_officers(self):
    return self._get_officer_group().user_set.all()
  def get_members(self):
    return self._get_member_group().user_set.all()

  def is_owner(self, user):
    return user in self._get_owner_group().user_set.all()
  def is_officer(self, user):
    return user in self._get_officer_group().user_set.all()
  def is_member(self, user):
    return user in self._get_member_group().user_set.all()

  def get_group(self, user):
    group = []
    if self.is_owner(user):
      group = 'Owner'
    elif self.is_officer(user):
      group = 'Officer'
    elif self.is_member(user):
      group = 'Member'
    return group

  def add_member(self, actor, user):
    '''
    return: True if user is member of the club, False if not
    '''
    if not 'can_handle_join_requests' in get_perms(actor, self):
      return False

    if user.groups.filter(name=self._get_member_group_name()).count() == 0:
      user.groups.add(self._get_member_group())
      self.members.add(user)

    return True

  def remove_member(self, actor, user):
    '''
    return: True if user removed, False if not
    '''
    if self.is_owner(user) and self.get_owners().count() <= 1:
       return False

    if 'can_remove_member' in get_perms(actor, self) or actor is user:
      # TODO edge case where actor and user is owner of club
      if user.groups.filter(name=self._get_owner_group_name()).count() > 0:
        user.groups.remove(self._get_owner_group())
      if user.groups.filter(name=self._get_officer_group_name()).count() > 0:
        user.groups.remove(self._get_officer_group())
      if user.groups.filter(name=self._get_member_group_name()).count() > 0:
        user.groups.remove(self._get_member_group())
      self.members.remove(user)
      return True # denotes the member was removed
    else:
      return False

    return False # denotes the member was not removed for some reason

  def promote_to_officer(self, actor, user):
    '''
    actor must have 'can_handle_promotion_requests' permission
    return: True if user now an officer, False if not
    '''
    is_member = self.is_member(user)
    if not is_member:
      return False
    if not 'can_handle_promotion_requests' in get_perms(actor, self):
      return False

    if user.groups.filter(name=self._get_officer_group_name()).count() == 0:
      user.groups.add(self._get_officer_group())
      return True

    return False

  def demote_from_officer(self, actor, user):
    '''
    actor must have 'can_handle_promotion_requests' permission
    '''
    is_officer = self.is_officer(user)
    if not is_officer:
      return False
    if not 'can_handle_promotion_requests' in get_perms(actor,self):
      return False

    if user.groups.filter(name=self._get_member_group_name()).count() == 0:
      user.groups.add(self._get_member_group())
      user.groups.remove(self._get_officer_group())

    if user.groups.filter(name=self._get_officer_group_name()).count() != 0:
      user.groups.remove(self._get_officer_group())
      return True

    return False

  def promote_officer_to_owner(self, actor, user):
    if not self.is_owner(actor):
       return False
    if not self.is_officer(user):
       return False
    if user.groups.filter(name=self._get_owner_group_name()).count() == 0:
       user.groups.add(self._get_owner_group())
       user.groups.remove(self._get_officer_group())
       return True

    return False

  def demote_owner_to_officer(self, actor, user):
    if not self.is_owner(actor):
       return False
    if not self.is_owner(user):
       return False
    if self.get_owners().count() <= 1:
       return False

    if user.groups.filter(name=self._get_owner_group_name()).count() != 0:
       user.groups.add(self._get_officer_group())
       user.groups.remove(self._get_owner_group())
       return True

    return False

  def _assign_member_permissions(self, group):
    assign_perm('can_request_reimbursement', group, self)

  def _assign_officer_permissions(self, group):
    assign_perm('can_handle_join_requests', group, self)
    assign_perm('can_view_stats', group, self)
    assign_perm('can_create_event', group, self)
    assign_perm('can_add_receipt', group, self)
    assign_perm('can_remove_receipt', group, self)
    assign_perm('can_access_attendance', group, self)
    assign_perm('can_access_budget', group, self)
    assign_perm('can_create_budget', group, self)
    assign_perm('can_request_reimbursement', group, self)
    assign_perm('can_view_account_info', group, self)

  def _assign_owner_permissions(self, group):
    assign_perm('can_remove_member', group, self)
    assign_perm('can_handle_promotion_requests', group, self)

    assign_perm('can_handle_join_requests', group, self)
    assign_perm('can_view_stats', group, self)
    assign_perm('can_create_event', group, self)
    assign_perm('can_add_receipt', group, self)
    assign_perm('can_remove_receipt', group, self)
    assign_perm('can_access_attendance', group, self)
    assign_perm('can_access_budget', group, self)
    assign_perm('can_create_budget', group, self)
    assign_perm('can_request_reimbursement', group, self)
    assign_perm('can_view_account_info', group, self)

  def _set_owner(self, user):
    '''
    Must and should only be called on club creation!!!
    '''
    user.groups.add(self._get_member_group())
    user.groups.add(self._get_officer_group())
    user.groups.add(self._get_owner_group())

    self.members.add(user)

  def _create_permissions(self):
    '''
    Must and should only be called on club creation!!!
    '''
    owner_group = Group.objects.create(name=self._get_owner_group_name())
    officer_group = Group.objects.create(name=self._get_officer_group_name())
    member_group = Group.objects.create(name=self._get_member_group_name())

    # Owners, officers, and members have all member permissions.
    self._assign_member_permissions(owner_group)
    self._assign_member_permissions(officer_group)
    self._assign_member_permissions(member_group)

    # Owners and officers have all officer permissions.
    self._assign_officer_permissions(owner_group)
    self._assign_officer_permissions(officer_group)

    # Only owners have all owner permissions.
    self._assign_owner_permissions(owner_group)

  def _clear_permissions(self):
    '''
    Must and should only be called on club deletion!!!
    '''
    owners = self.get_owners()
    officers = self.get_officers()
    members = self.get_members()

    owner_group = self._get_owner_group()
    officer_group = self._get_officer_group()
    member_group = self._get_member_group()
    for owner in owners:
      owner.groups.remove(owner_group)
    for officer in officers:
      officer.groups.remove(officer_group)
    for member in members:
      member.groups.remove(member_group)

    owner_group.delete()
    officer_group.delete()
    member_group.delete()

  def save(self, *args, **kwargs):
    if not self.first_seen:
      self.first_seen = timezone.now()
      self.last_seen = timezone.now()

    return super(Club, self).save(*args, **kwargs)
