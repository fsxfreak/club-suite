from .mdl_role import *

def qry_clubmembers(in_cid):
    club_members = Role.objects.filter(cid=in_cid)
    return club_members
