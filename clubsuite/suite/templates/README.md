# creating new templates 

Let's say I want to create a template containing all the CSS imports. Because
it would be *extended* from most every other template, it should serve as a
**base** and so I'd name it `base_css.html'

For templates intended to be directly rendered by a view,
if I created a `TemplateView` called `Index` in `views/view_index.py`, then I
will create a corresponding template html called `index.html`.

Don't forget to fill out optional `block`s, such as `{% block title %}` or
`{% block body_block %}`.

