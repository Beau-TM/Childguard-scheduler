from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('childguard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='slot',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='problems',
                to='childguard.supervisionslot',
                verbose_name='Bewakingsslot',
            ),
        ),
    ]
