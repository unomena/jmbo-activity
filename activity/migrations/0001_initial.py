# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PointsActivity'
        db.create_table('activity_pointsactivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('activity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
            ('points', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('limit_per_day', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('activity', ['PointsActivity'])

        # Adding model 'UserActivity'
        db.create_table('activity_useractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('sub', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('content_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_activity_content_object', null=True, to=orm['contenttypes.ContentType'])),
            ('content_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('image_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_activity_image_object', null=True, to=orm['contenttypes.ContentType'])),
            ('image_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('points_override', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('over_limit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('checked_for_badges', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('activity', ['UserActivity'])

        # Adding model 'Badge'
        db.create_table('activity_badge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('date_taken', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('crop_from', self.gf('django.db.models.fields.CharField')(default='center', max_length=10, blank=True)),
            ('effect', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='badge_related', null=True, to=orm['photologue.PhotoEffect'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('activity', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('threshold', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('activity', ['Badge'])

        # Adding unique constraint on 'Badge', fields ['activity', 'threshold']
        db.create_unique('activity_badge', ['activity', 'threshold'])

        # Adding model 'MemberBadge'
        db.create_table('activity_memberbadge', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foundry.Member'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Badge'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('activity', ['MemberBadge'])

        # Adding unique constraint on 'MemberBadge', fields ['member', 'badge']
        db.create_unique('activity_memberbadge', ['member_id', 'badge_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'MemberBadge', fields ['member', 'badge']
        db.delete_unique('activity_memberbadge', ['member_id', 'badge_id'])

        # Removing unique constraint on 'Badge', fields ['activity', 'threshold']
        db.delete_unique('activity_badge', ['activity', 'threshold'])

        # Deleting model 'PointsActivity'
        db.delete_table('activity_pointsactivity')

        # Deleting model 'UserActivity'
        db.delete_table('activity_useractivity')

        # Deleting model 'Badge'
        db.delete_table('activity_badge')

        # Deleting model 'MemberBadge'
        db.delete_table('activity_memberbadge')


    models = {
        'activity.badge': {
            'Meta': {'unique_together': "(('activity', 'threshold'),)", 'object_name': 'Badge'},
            'activity': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'badge_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'threshold': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'activity.memberbadge': {
            'Meta': {'unique_together': "(('member', 'badge'),)", 'object_name': 'MemberBadge'},
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Badge']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['foundry.Member']"})
        },
        'activity.pointsactivity': {
            'Meta': {'ordering': "['points']", 'object_name': 'PointsActivity'},
            'activity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_per_day': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'points': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'activity.useractivity': {
            'Meta': {'object_name': 'UserActivity'},
            'activity': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'checked_for_badges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_activity_content_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'content_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_activity_image_object'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"}),
            'image_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'over_limit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'points_override': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sub': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
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
        'foundry.country': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Country'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum_age': ('django.db.models.fields.PositiveIntegerField', [], {'default': '18'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '32', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'foundry.member': {
            'Meta': {'object_name': 'Member', '_ormbases': ['auth.User']},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['foundry.Country']", 'null': 'True', 'blank': 'True'}),
            'crop_from': ('django.db.models.fields.CharField', [], {'default': "'center'", 'max_length': '10', 'blank': 'True'}),
            'date_taken': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'effect': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'member_related'", 'null': 'True', 'to': "orm['photologue.PhotoEffect']"}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'twitter_username': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'photologue.photoeffect': {
            'Meta': {'object_name': 'PhotoEffect'},
            'background_color': ('django.db.models.fields.CharField', [], {'default': "'#FFFFFF'", 'max_length': '7'}),
            'brightness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'color': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'contrast': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filters': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'reflection_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'reflection_strength': ('django.db.models.fields.FloatField', [], {'default': '0.59999999999999998'}),
            'sharpness': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'transpose_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }

    complete_apps = ['activity']
