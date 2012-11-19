# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('submissions_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
        ))
        db.send_create_signal('submissions', ['Category'])

        # Adding model 'Entry'
        db.create_table('submissions_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['submissions.Category'], unique=True)),
        ))
        db.send_create_signal('submissions', ['Entry'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('submissions_category')

        # Deleting model 'Entry'
        db.delete_table('submissions_entry')


    models = {
        'submissions.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'submissions.entry': {
            'Meta': {'object_name': 'Entry'},
            'category': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['submissions.Category']", 'unique': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['submissions']