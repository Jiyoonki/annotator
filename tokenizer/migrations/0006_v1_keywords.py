# Generated by Django 3.0.3 on 2020-07-20 10:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0005_auto_20200715_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='v1_Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('session_id', models.CharField(max_length=100)),
                ('session_index', models.IntegerField()),
                ('text', models.TextField()),
                ('words', models.TextField()),
                ('words_selected', models.TextField()),
                ('keywords', models.TextField(null=True)),
            ],
        ),
    ]
