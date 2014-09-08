django-simple-activity
======================

[![Build Status](https://travis-ci.org/richardasaurus/django-simple-activity.png?branch=master)](https://travis-ci.org/richardasaurus/django-simple-activity)
[![Downloads](https://pypip.in/d/django-simple-activity/badge.png)](https://crate.io/packages/django-simple-activity/)

Simple, generic, activity streams from the actions on your site.

## Installation

Install using `pip`...

```pip install django-simple-activity```

Add `'activity'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'activity',
)
```


## Example Usage

The best examples are in the [tests](https://github.com/richardasaurus/django-simple-activity/blob/master/src/tests/test_activity.py).


Get **all** Activity Action records:

```python
Action.objects.all()
```


Get all **public** Activity Action records:
```python
Action.objects.public()
```

Get all **private** Activity Action records, where the actor is a given user

```python
Action.objects.private(actor=user)  # user being a Django User model instance
```

Here's an example use of `django-simple-activity` which uses [django signals](https://docs.djangoproject.com/en/dev/topics/signals/)
to trigger off the creation of an activity action when a new user registers on the site.


```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from activity.logic import add_action
from . models import UserProfile


@receiver(pre_save, sender=UserProfile)
def new_user_activity(sender, **kwargs):
    profile = kwargs.get('instance')
    # if no profile.id yet, then this is a new user registering
    if not profile.id:
        add_action(actor=profile.user, verb='joined the website!')
```


## Running the unit tests

To test dependency installation and run the tests:

```
pip install tox
tox
```
