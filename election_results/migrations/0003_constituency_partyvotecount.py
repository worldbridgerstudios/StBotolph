# Generated by Django 5.0.1 on 2024-01-31 20:27

import django.db.models.deletion
import election_results.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('election_results', '0002_auto_20240131_0440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
            bases=(models.Model, election_results.models.OrderByNameMixin),
        ),
        migrations.CreateModel(
            name='PartyVoteCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_counts', to='election_results.constituency')),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_counts', to='election_results.party')),
            ],
        ),
    ]
