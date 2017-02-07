# creating new views

If I wanted to create a new CreateEventBudget view, I would create 
```view_create_event_budget.py```,
and continue to write the view function as normal. Then I would open
```__init__.py``` and add ```from .view_create_event_budget import *```.

Don't forget to add to clubsuite/suite/urls.py the new view. For example,
I would add to the ```urlpatterns``` array, 
```python
url(r'^create/event/budget$', views.CreateEventBudget.as_view(), name='create_event_budget')
```
There are different ways to treat class-based views and function based views.
Above I just demonstrated using a class-based view.

Note that we don't have to create a new file for every view. We can group
related views together. For example, if I wanted to create views for logging in,
changing password, updating user account information, I could group them
under `view_user_accounts.py`.

Try to inherit views when possible. For example, it seems like
`GeneralDashboard` could inherit from `Dashboard`. We'll see in the design.
