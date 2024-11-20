# Generated by Django 4.2.16 on 2024-11-20 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="InvestmentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=15)),
                ("investment_period", models.IntegerField()),
                ("preferred_banks", models.TextField(blank=True, null=True)),
                ("risk_preference", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="PlanItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("product_type", models.CharField(max_length=20)),
                ("product_id", models.TextField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=15)),
                ("start_month", models.IntegerField()),
                ("period", models.IntegerField()),
                (
                    "expected_return",
                    models.DecimalField(decimal_places=2, max_digits=15),
                ),
                (
                    "plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="recommendations.investmentplan",
                    ),
                ),
            ],
        ),
    ]
