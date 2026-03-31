from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Registration, Event


@receiver(post_save, sender=Registration)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        event = instance.event

        subject = f"Registration Confirmation: {event.title}"
        message = (
            f"Hello {user.username},\n\n"
            f"You have successfully registered for the event '{event.title}'.\n\n"
            f"Event Details:\n"
            f"- Date & Time: {event.date.strftime('%Y-%m-%d at %H:%M')}\n"
            f"- Location: {event.location}\n\n"
            f"Best regards,\n"
            f"Event Planner API"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )


@receiver(post_save, sender=Event)
def send_event_creation_email(sender, instance, created, **kwargs):
    if created:
        organizer = instance.organizer

        subject = f"Event Created: {instance.title}"

        message = (
            f"Hello {organizer.username},\n\n"
            f"You have successfully created the event '{instance.title}'.\n\n"
            f"Event Details:\n"
            f"- Date & Time: {instance.date.strftime('%Y-%m-%d at %H:%M')}\n"
            f"- Location: {instance.location}\n\n"
            f"You will be able to see all registered attendees in your dashboard.\n\n"
            f"Best regards,\n"
            f"Event Planner API"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[organizer.email],
            fail_silently=False,
        )