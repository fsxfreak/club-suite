from .mdl_role import *

def qry_clubmembers(in_cid):
    club_users = Role.objects.filter(cid=in_cid)
    club_members = club_users.exclude(title='P')
    return club_members
