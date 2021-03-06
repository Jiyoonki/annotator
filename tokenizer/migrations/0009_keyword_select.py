# Generated by Django 3.0.3 on 2020-07-28 09:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tokenizer', '0008_auto_20200720_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='keyword_select',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.CharField(max_length=100)),
                ('user_key', models.IntegerField()),
                ('author_id', models.CharField(max_length=100)),
                ('pos_text', models.TextField()),
                ('neg_text', models.TextField()),
                ('pos_text_norm', models.TextField()),
                ('neg_text_norm', models.TextField()),
                ('pos_keyword', models.TextField()),
                ('neg_keyword', models.TextField()),
                ('pos_word_num', models.TextField()),
                ('neg_word_num', models.TextField()),
                ('rand_order', models.IntegerField()),
            ],
        ),
    ]
