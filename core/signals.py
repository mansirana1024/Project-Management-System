from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import *


@receiver(post_save, sender=Schedule)
def schedule_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            text="New schedule added by the admin",
            title="New Schedule",
            receiver="supervisors",
        )


@receiver(post_save, sender=Project)
def project_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            text="New project <strong>{}</strong> added. Reach out to the coordinator if you want to supervise this project.".format(
                instance.title
            ),
            title="New project added",
            receiver="supervisors",
        )


@receiver(post_save, sender=Student)
def student_supervisor_notification(sender, instance, created, **kwargs):
    if instance.supervisor:
        Notification.objects.create(
            text="The project <strong>{}</strong> by <strong>{}</strong> has been assigned to <strong>{}</strong>.".format(
                instance.project.title,
                instance.user.get_full_name(),
                instance.supervisor.user.get_full_name(),
            ),
            title="Project Supervisor Assigned",
            receiver="everyone",
        )


@receiver(post_save, sender=Milestone)
def milestone_created_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            text="New milestone added by the coordinator. Click on project schedule to find out.",
            title="New Milestone Added",
            receiver="students",
        )
