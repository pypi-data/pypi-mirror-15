Django Custom Settings
======================

# FAQ

* What does this do?

> Register your custom standalone app settings into Django conf, so they can be overrided by users of your standalone app.

* How does it work?

> Create a settings.py in your app. Make sure your settings are all caps.
> In your init file for you app, add a call to django-custom-settings and you're done.

# Full Example

```python
# __init__.py
from custom_settings.loader import load_settings
load_settings(__name__)
```

```python
# settings.py
MYAPP_SETTINGS_FOO = "foo"
MYAPP_SETTINGS_BAR = "bar"

myapp_settings_that_wont_be_loaded = "will not be available, because it's not all uppercase"
```

```python
# usage, on views.py, for example
from django.conf import settings

def home(request):
    
    if settings.MYAPP_SETTINGS_FOO == "foo":
        return "this is a foo"
    else:
        return "this is not a foo"
```