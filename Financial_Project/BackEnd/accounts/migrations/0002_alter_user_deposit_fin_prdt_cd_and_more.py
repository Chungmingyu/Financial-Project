# Generated by Django 4.2.16 on 2024-11-20 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moneys', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deposit_fin_prdt_cd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deposit', to='moneys.depositproduct'),
        ),
        migrations.AlterField(
            model_name='user',
            name='saving_fin_prdt_cd',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saving', to='moneys.savingproduct'),
        ),
    ]
