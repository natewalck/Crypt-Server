# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 16:00
from __future__ import unicode_literals

from server.models import *
from django.db import migrations, models


def unique_serials(apps, schema_editor):
    """
    Make sure serial numbers are unique
    """
    seen_serials = []
    Computer = apps.get_model("server", "Computer")
    Secret = apps.get_model("server", "Secret")
    all_computers = Computer.objects.all()
    for computer in all_computers:
        if computer.serial not in seen_serials:
            # not seen it before, add it to the list of devices we've seen
            seen_serials.append(computer.serial)
        else:
            # we've seen it before, select all the secrets for the
            # machine and move them to the first instance of the serial number
            secrets = Secret.objects.filter(computer=computer)
            # reselect here so we don't get bit when we delete the computer
            first_computer = Computer.objects.all().first()
            for secret in secrets:
                secret.computer = first_computer
                secret.save()
            computer.delete()


class Migration(migrations.Migration):

    dependencies = [("server", "0009_secret_rotation_required")]

    operations = [migrations.RunPython(unique_serials)]
