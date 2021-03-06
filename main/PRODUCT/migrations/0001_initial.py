# Generated by Django 3.2.4 on 2021-07-11 03:23

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(choices=[('Fast Food', 'Fast Food'), ('Meal', 'Meal'), ('Dinner', 'Dinner'), ('Cookies', 'Cookies')], default='meal', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('custom_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('image1', models.ImageField(upload_to='media/plantimage/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='media/plantimage/')),
                ('description', models.TextField(max_length=1000)),
                ('max_price', models.PositiveIntegerField(default=1)),
                ('off_price', models.PositiveIntegerField(default=1)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('Sub_catagory_p', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PRODUCT.catagory')),
            ],
        ),
    ]
