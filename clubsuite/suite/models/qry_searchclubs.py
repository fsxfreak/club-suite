from .mdl_club import *
from django.db.models import Q

def qry_searchclubs(keyword):
    r=Club.objects.filter(
        Q(club_name__contains=keyword) |
        Q(club_description__contains=keyword)
    )
    return r
        
