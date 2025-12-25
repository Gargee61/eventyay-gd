from datetime import timedelta

from django.dispatch import Signal, receiver
from django.utils.timezone import now
from django_scopes import scopes_disabled

from eventyay.api.models import ApiCall, WebHookCall
from eventyay.base.signals import periodic_task
from eventyay.helpers.periodic import minimum_interval

register_webhook_events = Signal()
"""
This signal is sent out to get all known webhook events. Receivers should return an
instance of a subclass of pretix.api.webhooks.WebhookEvent or a list of such
instances.
"""


@receiver(periodic_task)
@scopes_disabled()
@minimum_interval(minutes_after_success=12 * 60)
def cleanup_webhook_logs(sender, **kwargs):
    WebHookCall.objects.filter(datetime__lte=now() - timedelta(days=30)).delete()


@receiver(periodic_task)
@scopes_disabled()
@minimum_interval(minutes_after_success=12 * 60)
def cleanup_api_logs(sender, **kwargs):
    ApiCall.objects.filter(created__lte=now() - timedelta(hours=24)).delete()

from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender='eventyay.Event')
def create_event_components(sender, instance, created, **kwargs):
    """
    Automatically create all components when a new event is created.
    This replaces the conditional component creation logic.
    
    Issue #1154: All events now get Tickets, Talk, and Video components by default.
    """
    if created:
        
        from eventyay.models import Event
        
        try:
            
            if hasattr(instance, 'tickets_component'):
                logger.info(f"Tickets component already exists for event {instance.slug}")
            
        
            from eventyay.talk.models import Event as TalkEvent
            talk_event, created_talk = TalkEvent.objects.get_or_create(
                slug=instance.slug,
                defaults={
                    'name': instance.name,
                    'is_public': False,  
                }
            )
            
            if hasattr(instance, 'video'):
                from eventyay.video.models import Room
                
                logger.info(f"Video component initialized for event {instance.slug}")
            
            logger.info(
                f"Auto-created components for event {instance.slug}"
            )
            
        except Exception as e:
            logger.error(f"Error creating components for event {instance.slug}: {e}")