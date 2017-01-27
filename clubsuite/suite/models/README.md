# creating new models

If I wanted to create a new ClubPresident model, I would create 
```mdl_club_president.py```, and within it ```from django.db import models```,
and continue to write the model class as normal. Then I would open
```__init__.py``` and add ```from .mdl_club_president import *```.
