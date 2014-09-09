from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.humanize.templatetags.humanize import naturaltime
from model_utils.managers import PassThroughManager
from . querysets import ActionQueryset


class Action(models.Model):
    # The object which performed the activity
    actor_content_type = models.ForeignKey(
        ContentType, related_name='actor', blank=True, null=True
    )
    actor_object_id = models.CharField(max_length=500, blank=True, null=True)
    actor = generic.GenericForeignKey(
        ct_field='actor_content_type', fk_field='actor_object_id'
    )
    # The phrase describing the action of that activity
    verb = models.CharField(max_length=500)

    # The object which is linked to the action (e.g. liked, favourited)
    action_content_type = models.ForeignKey(
        ContentType, related_name='action', blank=True, null=True
    )
    action_object_id = models.CharField(max_length=500, blank=True, null=True)
    action = generic.GenericForeignKey(
        ct_field='action_content_type', fk_field='action_object_id'
    )

    # The object on which the action was performed upon (e.g. a fb page)
    target_content_type = models.ForeignKey(
        ContentType, related_name='target', blank=True, null=True
    )
    target_object_id = models.CharField(max_length=500, blank=True, null=True)
    target = generic.GenericForeignKey(
        ct_field='target_content_type', fk_field='target_object_id'
    )

    is_public = models.BooleanField(default=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True)
    objects = PassThroughManager.for_queryset_class(ActionQueryset)()

    @property
    def time_ago(self):
        # human readable time ago, e.g. 5 hours ago
        return naturaltime(self.timestamp)

    class Meta:
        ordering = ('-timestamp', )
        app_label = 'activity'
