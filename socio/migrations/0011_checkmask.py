# Generated by Django 2.2.6 on 2020-06-19 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socio', '0010_delete_checkmask'),
    ]

    operations = [
        migrations.CreateModel(
            name='checkmask',
            fields=[
                ('mid', models.AutoField(primary_key=True, serialize=False)),
                ('d_image', models.ImageField(upload_to='detected')),
            ],
        ),
    ]
