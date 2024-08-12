# Generated by Django 5.0.7 on 2024-08-12 00:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_alter_like_unique_together_remove_like_travel_plan_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelplan',
            name='comment_count',
        ),
        migrations.AlterField(
            model_name='planlike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='travelplan',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_plans', to=settings.AUTH_USER_MODEL),
        ),
    ]
