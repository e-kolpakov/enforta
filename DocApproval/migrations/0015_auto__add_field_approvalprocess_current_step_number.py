# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ApprovalProcess.current_step_number'
        db.add_column(u'DocApproval_approvalprocess', 'current_step_number',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ApprovalProcess.current_step_number'
        db.delete_column(u'DocApproval_approvalprocess', 'current_step_number')


    models = {
        u'DocApproval.approvalprocess': {
            'Meta': {'object_name': 'ApprovalProcess'},
            'attempt_number': ('django.db.models.fields.IntegerField', [], {}),
            'current_step_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'processes'", 'to': u"orm['DocApproval.ApprovalRoute']"})
        },
        u'DocApproval.approvalprocessaction': {
            'Meta': {'object_name': 'ApprovalProcessAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'action_taken': ('django.db.models.fields.DateTimeField', [], {}),
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actions'", 'to': u"orm['DocApproval.ApprovalProcess']"}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.ApprovalRouteStep']"})
        },
        u'DocApproval.approvalroute': {
            'Meta': {'object_name': 'ApprovalRoute'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'DocApproval.approvalroutestep': {
            'Meta': {'object_name': 'ApprovalRouteStep'},
            'approver': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.UserProfile']", 'null': 'True'}),
            'calc_step': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'steps'", 'to': u"orm['DocApproval.ApprovalRoute']"}),
            'step_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'DocApproval.city': {
            'Meta': {'object_name': 'City'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'DocApproval.contract': {
            'Meta': {'object_name': 'Contract'},
            'activation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'active_period': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'document_signed': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'prolongation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'DocApproval.position': {
            'Meta': {'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        u'DocApproval.request': {
            'Meta': {'object_name': 'Request'},
            'accepted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'approval_route': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['DocApproval.ApprovalRoute']", 'unique': 'True', 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.City']"}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'request'", 'unique': 'True', 'to': u"orm['DocApproval.Contract']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests'", 'to': u"orm['DocApproval.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updater': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests_last_updated_by'", 'to': u"orm['DocApproval.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'send_on_approval': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests_to_be_sent_on_approval'", 'to': u"orm['DocApproval.UserProfile']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.RequestStatus']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'DocApproval.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'status_name': ('django.db.models.fields.CharField', [], {'max_length': '800'})
        },
        u'DocApproval.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.City']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '800'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'first_name_accusative': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'last_name_accusative': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'middle_name_accusative': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.Position']"}),
            'sign': ('django.db.models.fields.files.ImageField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['DocApproval']