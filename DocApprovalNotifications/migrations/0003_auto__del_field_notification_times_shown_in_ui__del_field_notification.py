# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting field 'Notification.times_shown_in_ui'
        db.delete_column(u'DocApprovalNotifications_notification', 'times_shown_in_ui')

        # Deleting field 'Notification.processed'
        db.delete_column(u'DocApprovalNotifications_notification', 'processed')

        # Adding field 'Notification.dismissed'
        db.add_column(u'DocApprovalNotifications_notification', 'dismissed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.ui_dismissed'
        db.add_column(u'DocApprovalNotifications_notification', 'ui_dismissed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.notification_type'
        db.add_column(u'DocApprovalNotifications_notification', 'notification_type',
                      self.gf('django.db.models.fields.CharField')(default='APPROVE_REQUIRED', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Notification.times_shown_in_ui'
        db.add_column(u'DocApprovalNotifications_notification', 'times_shown_in_ui',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Notification.processed'
        db.add_column(u'DocApprovalNotifications_notification', 'processed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Notification.dismissed'
        db.delete_column(u'DocApprovalNotifications_notification', 'dismissed')

        # Deleting field 'Notification.ui_dismissed'
        db.delete_column(u'DocApprovalNotifications_notification', 'ui_dismissed')

        # Deleting field 'Notification.notification_type'
        db.delete_column(u'DocApprovalNotifications_notification', 'notification_type')


    models = {
        'DocApproval.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        'DocApproval.position': {
            'Meta': {'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        'DocApproval.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '800'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name_accusative': (
            'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'last_name_accusative': (
            'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': "orm['DocApproval.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'middle_name_accusative': (
            'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.Position']"}),
            'sign': (
            'django.db.models.fields.files.ImageField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [],
                     {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'DocApprovalNotifications.event': {
            'Meta': {'object_name': 'Event'},
            'entity': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'entity_id': ('django.db.models.fields.IntegerField', [], {}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'params': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'sender': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.UserProfile']", 'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'DocApprovalNotifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'dismissed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApprovalNotifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_recipient': (
            'django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.UserProfile']", 'null': 'True'}),
            'notification_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repeating': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ui_dismissed': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
            'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['DocApprovalNotifications']