# creating new views

If I wanted to create a new CreateEventBudget view, I would create 
```view_create_event_budget.py```,
and continue to write the view function as normal. Then I would open
```__init__.py``` and add ```from .view_create_event_budget import *```.

Don't forget to add to clubsuite/suite/urls.py the new view. For example,
I would add to the ```urlpatterns``` array, 
```
url(r'^create/event/budget$', views.create_event_budget.index, name='create_event_budget')
Notice that ```index``` should correspond to the name of the function that you
defined as in view.
