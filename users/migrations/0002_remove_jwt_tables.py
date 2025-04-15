from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            # Удаляем таблицы JWT
            sql="""
            DROP TABLE IF EXISTS token_blacklist_outstandingtoken CASCADE;
            DROP TABLE IF EXISTS token_blacklist_blacklistedtoken CASCADE;
            """,
            # Откат не нужен, так как мы удаляем таблицы
            reverse_sql=""
        ),
    ]