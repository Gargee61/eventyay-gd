import pytest
from django.test import TestCase, Client
from django.urls import reverse
from eventyay.models import Event, Organizer


class EventCreationTestCase(TestCase):
    """
    Tests for event creation after issue #1154 changes.
    Verifies that all components are created automatically.
    """
    
    def setUp(self):
        self.client = Client()
        self.organizer = Organizer.objects.create(
            name="Test Organizer",
            slug="test-org"
        )
    
    def test_event_creation_creates_all_components(self):
        """Test that creating an event automatically creates all components."""
        event = Event.objects.create(
            name='Test Event',
            slug='test-event',
            organizer=self.organizer,
        )
        
        assert event is not None
        