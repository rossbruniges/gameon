# encoding: utf-8
from south.v2 import DataMigration
from django.core.exceptions import ObjectDoesNotExist

LOCATIONS = (
    {
        'id': 1,
        'name': 'Mozilla London',
        'street': '101 St Martins Lane',
        'town': 'London',
        'country': 'UK'
    },
    {
        'id': 2,
        'name': 'D12 Parsons The New School for Design',
        'street': '10011, 12th Floor, 6 East 16th Street',
        'town': 'New York',
        'country': 'USA'
    },
)

EVENTS = (
    {
        'name': 'Game On! Game Jam',
        'url': 'http://gameonjam.eventbrite.co.uk/',
        'location_id': 1,
        'start_date': '2012-12-14 18:00:00',
        'end_date': '2012-12-16 18:00:00'
    },
    {
        'name': 'Game On! Mozilla Game Jamming',
        'url': 'http://gameonjamnyc.eventbrite.co.uk/',
        'location_id': 2,
        'start_date': '2012-12-14 18:30:00',
        'end_date': '2012-12-16 19:00:00'
    },
)


class Migration(DataMigration):

    depends_on = (
        ('submissions', '0006_auto__chg_field_category_description__chg_field_challenge_slug'),
        )

    def forwards(self, orm):
        for loc in LOCATIONS:
            try:
                location = (orm['events.Location'].objects
                            .get(name=loc['name']))
            except ObjectDoesNotExist:
                category_data = {
                    'id': loc['id'],
                    'name': loc['name'],
                    'street': loc['street'],
                    'town': loc['town'],
                    'country': loc['country']
                    }
                location = orm['events.Location'].objects.create(**category_data)

        for ev in EVENTS:
            try:
                event = (orm['events.Event'].objects
                            .get(url=ev['url']))
            except ObjectDoesNotExist:
                category_data = {
                    'name': ev['name'],
                    'url': ev['url'],
                    'location_id': ev['location_id'],
                    'start_date': ev['start_date'],
                    'end_date': ev['end_date']
                    }
                event = orm['events.Event'].objects.create(**category_data)

    def backwards(self, orm):
        "Write your backwards methods here."
        print "Not removing any data from the DB, we can't know for certain what was there before"
        pass

    models = {
        'events.event': {
            'Meta': {'object_name': 'Event'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['events.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'events.location': {
            'Meta': {'object_name': 'Location'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['events']
