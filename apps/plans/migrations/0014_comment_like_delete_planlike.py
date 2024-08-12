# Generated by Django 5.0.7 on 2024-08-12 01:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0013_travelplan_comment_count_alter_planlike_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('travel_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='plans.travelplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('travel_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='plans.travelplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plans.userprofile')),
            ],
            options={
                'unique_together': {('user', 'travel_plan')},
            },
        ),
        migrations.DeleteModel(
            name='PlanLike',
        ),
    ]
