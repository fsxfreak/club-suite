from .mdl_club import *

    def qry_searchclubs(keyword):
        r = Club.objects.filter(club_name__contains=keyword).\
            filter(club_description__contains=keyword)
        return r
        
