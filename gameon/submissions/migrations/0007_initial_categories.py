# encoding: utf-8
from south.v2 import DataMigration
from django.core.exceptions import ObjectDoesNotExist

CATEGORIES = (
    {
        'title': 'Multi-Device Games',
        'slug': 'multi-device-games',
        'desc': 'Use the power of mobile to explore concepts like asymmetric gaming, alternate reality games, and companion apps. This category is searching for games that take advantage of the unique affordances of different platforms they inhabit.',
        'award': 'Awarded to the game that explores best concepts like asymmetric gaming, alternate reality games, and companion apps. This category is searching for games that take advantage of the unique affordances of different platforms they inhabit.'
    },
    {
        'title': 'Web-Only Games',
        'slug': 'web-only-games',
        'desc': 'Create games that can only be played on the web. Get inspired by web-only mechanics such as sharing links and data, finding clues on the web that will help you advance in the game, always-on multi-player, and more—creating the most webilicious game possible!',
        'award': 'Awarded to the game that pushes the limits of what is possible on the web. Get inspired by web-only mechanics such as sharing links and data, finding clues on the web that will help you advance in the game, always-on multi-player, and more—creating the most webilicious game possible!'
    },
    {
        'title': 'Hackable Games',
        'slug': 'hackable-games',
        'desc': 'Create games that let players remix game mechanics, fork code, or use assets from the web to create their own version (and maybe even learn how to code along the way).',
        'award': 'Awarded to the game with the highest "hackability" score. Hackable Games let their players remix mechanics, fork code or use assets from the web in order for them to create their very own version of an existing game. (and maybe even learn how to code along the way).'
    },
)


class Migration(DataMigration):

    depends_on = (
        ('submissions', '0006_auto__chg_field_category_description__chg_field_challenge_slug'),
        )

    def forwards(self, orm):
        for cat in CATEGORIES:
            try:
                category = (orm['submissions.Category'].objects
                            .get(slug=cat['slug']))
            except ObjectDoesNotExist:
                category_data = {
                    'name': cat['title'],
                    'slug': cat['slug'],
                    'description': cat['desc'],
                    }
                category = orm['submissions.Category'].objects.create(**category_data)

    def backwards(self, orm):
        "Write your backwards methods here."
        print "Not removing any data from the DB, we can't know for certain what was there before"
        pass

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'submissions.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'submissions.challenge': {
            'Meta': {'object_name': 'Challenge'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '200'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'submissions.entry': {
            'Meta': {'object_name': 'Entry'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['submissions.Category']", 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.Profile']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'team_desciption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_members': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'to_market': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'video_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255'})
        },
        'users.profile': {
            'Meta': {'object_name': 'Profile'},
            'bio': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['submissions']
