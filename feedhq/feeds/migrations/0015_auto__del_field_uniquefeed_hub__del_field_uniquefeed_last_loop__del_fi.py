# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from feedhq.utils import get_redis_connection
from rache import REDIS_KEY, job_key


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UniqueFeed.hub'
        db.delete_column(u'feeds_uniquefeed', 'hub')

        # Deleting field 'UniqueFeed.last_loop'
        db.delete_column(u'feeds_uniquefeed', 'last_loop')

        # Deleting field 'UniqueFeed.backoff_factor'
        db.delete_column(u'feeds_uniquefeed', 'backoff_factor')

        # Deleting field 'UniqueFeed.link'
        db.delete_column(u'feeds_uniquefeed', 'link')

        # Deleting field 'UniqueFeed.etag'
        db.delete_column(u'feeds_uniquefeed', 'etag')

        # Deleting field 'UniqueFeed.subscribers'
        db.delete_column(u'feeds_uniquefeed', 'subscribers')

        # Deleting field 'UniqueFeed.title'
        db.delete_column(u'feeds_uniquefeed', 'title')

        # Deleting field 'UniqueFeed.modified'
        db.delete_column(u'feeds_uniquefeed', 'modified')

        # Deleting field 'UniqueFeed.last_update'
        db.delete_column(u'feeds_uniquefeed', 'last_update')

        redis = get_redis_connection()
        jobs = redis.zrange(REDIS_KEY, 0, -1)
        for job in jobs:
            redis.hdel(job_key(job.decode('utf-8')), 'request_timeout')


    def backwards(self, orm):
        # Adding field 'UniqueFeed.hub'
        db.add_column(u'feeds_uniquefeed', 'hub',
                      self.gf('feedhq.feeds.fields.URLField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.last_loop'
        db.add_column(u'feeds_uniquefeed', 'last_loop',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.backoff_factor'
        db.add_column(u'feeds_uniquefeed', 'backoff_factor',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'UniqueFeed.link'
        db.add_column(u'feeds_uniquefeed', 'link',
                      self.gf('feedhq.feeds.fields.URLField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.etag'
        db.add_column(u'feeds_uniquefeed', 'etag',
                      self.gf('django.db.models.fields.CharField')(max_length=1023, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.subscribers'
        db.add_column(u'feeds_uniquefeed', 'subscribers',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.title'
        db.add_column(u'feeds_uniquefeed', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=2048, blank=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.modified'
        db.add_column(u'feeds_uniquefeed', 'modified',
                      self.gf('django.db.models.fields.CharField')(max_length=1023, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UniqueFeed.last_update'
        db.add_column(u'feeds_uniquefeed', 'last_update',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'feeds.category': {
            'Meta': {'ordering': "('order', 'name', 'id')", 'unique_together': "(('user', 'slug'), ('user', 'name'))", 'object_name': 'Category'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'db_index': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'categories'", 'to': u"orm['profiles.User']"})
        },
        u'feeds.entry': {
            'Meta': {'ordering': "('-date', '-id')", 'object_name': 'Entry', 'index_together': "(('user', 'date'), ('user', 'read'), ('user', 'starred'), ('user', 'broadcast'))"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '1023', 'blank': 'True'}),
            'broadcast': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'entries'", 'null': 'True', 'to': u"orm['feeds.Feed']"}),
            'guid': ('feedhq.feeds.fields.URLField', [], {'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('feedhq.feeds.fields.URLField', [], {'db_index': 'True'}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'read_later_url': ('feedhq.feeds.fields.URLField', [], {'blank': 'True'}),
            'starred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'subtitle': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': u"orm['profiles.User']"})
        },
        u'feeds.favicon': {
            'Meta': {'object_name': 'Favicon'},
            'favicon': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('feedhq.feeds.fields.URLField', [], {'unique': 'True', 'db_index': 'True'})
        },
        u'feeds.feed': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Feed'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'feeds'", 'null': 'True', 'to': u"orm['feeds.Category']"}),
            'favicon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img_safe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'unread_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'url': ('feedhq.feeds.fields.URLField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'to': u"orm['profiles.User']"})
        },
        u'feeds.uniquefeed': {
            'Meta': {'object_name': 'UniqueFeed'},
            'error': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_column': "'muted_reason'", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'muted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'url': ('feedhq.feeds.fields.URLField', [], {'unique': 'True'})
        },
        u'profiles.user': {
            'Meta': {'object_name': 'User', 'db_table': "'auth_user'"},
            'allow_media': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'endless_pages': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'entries_per_page': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'font': ('django.db.models.fields.CharField', [], {'default': "'palatino'", 'max_length': '75'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'oldest_first': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'read_later': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'read_later_credentials': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sharing_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sharing_gplus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sharing_twitter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '75'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        }
    }

    complete_apps = ['feeds']
