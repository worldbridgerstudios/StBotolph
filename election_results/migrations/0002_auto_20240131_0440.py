from django.db import migrations

def load_initial_party_data(apps, schema_editor):
    # Use historical Party model to avoid newer model conflicts with migration.
    Party = apps.get_model("election_results", "Party")
    # Initial party data provided by the project spec.
    initial_party_data = {
        "C": "Conservative Party",
        "L": "Labour Party",
        "UKIP": "UKIP",
        "LD": "Liberal Democrats",
        "G": "Green Party",
        "Ind": "Independent",
        "SNP": "SNP",
    }
    for code, name in initial_party_data.items():
        Party.objects.create(code=code, name=name)

class Migration(migrations.Migration):

    dependencies = [
        ('election_results', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_party_data),
    ]
