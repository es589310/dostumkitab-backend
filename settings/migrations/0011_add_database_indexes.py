# Generated manually for performance optimization
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('settings', '0010_sitesettings_coordinates'),
    ]

    operations = [
        # SiteSettings üçün index
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_sitesettings_active ON settings_sitesettings(is_active);",
            "DROP INDEX IF EXISTS idx_sitesettings_active;"
        ),
        # Logo üçün index
        migrations.RunSQL(
            "CREATE INDEX IF NOT EXISTS idx_logo_active ON settings_logo(is_active);",
            "DROP INDEX IF EXISTS idx_logo_active;"
        ),
    ] 