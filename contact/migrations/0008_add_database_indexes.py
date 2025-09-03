# Generated manually for performance optimization
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('contact', '0007_delete_sitesettings'),
    ]

    operations = [
        # SocialMediaLink üçün index-lər
        migrations.RunSQL(
            # Index yarad
            "CREATE INDEX IF NOT EXISTS idx_socialmedia_active_hidden ON contact_socialmedialink(is_active, is_hidden);",
            # Index sil (rollback üçün)
            "DROP INDEX IF EXISTS idx_socialmedia_active_hidden;"
        ),
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_socialmedia_order_platform ON contact_socialmedialink(\"order\", platform);",
            "DROP INDEX IF EXISTS idx_socialmedia_order_platform;"
        ),
        # ContactMessage üçün index
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_contactmessage_status ON contact_contactmessage(status);",
            "DROP INDEX IF EXISTS idx_contactmessage_status;"
        ),
    ] 