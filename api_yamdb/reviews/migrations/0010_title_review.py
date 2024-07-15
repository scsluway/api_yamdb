# Generated by Django 3.2 on 2024-07-13 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_comment_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='review',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='reviews.review'),
            preserve_default=False,
        ),
    ]