# Generated by Django 3.2.8 on 2024-10-01 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0013_jobapplymodel_jobmodel'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobmodel',
            options={'ordering': ['-posted_date']},
        ),
        migrations.RenameField(
            model_name='jobmodel',
            old_name='company_name',
            new_name='Company_name',
        ),
        migrations.RenameField(
            model_name='jobmodel',
            old_name='description',
            new_name='Description',
        ),
        migrations.RenameField(
            model_name='jobmodel',
            old_name='employment_type',
            new_name='Employment_type',
        ),
        migrations.RenameField(
            model_name='jobmodel',
            old_name='location',
            new_name='Location',
        ),
        migrations.RenameField(
            model_name='jobmodel',
            old_name='salary',
            new_name='Salary',
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='Requirements',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='company_logo',
            field=models.ImageField(null=True, upload_to='Media/Pro_pic'),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='jobmodel',
            name='qualification',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='jobmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
