# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'DocApproval_document')

        # Adding model 'Contract'
        db.create_table(u'DocApproval_contract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('active_period', self.gf('django.db.models.fields.IntegerField')()),
            ('prolongation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_date', self.gf('django.db.models.fields.DateField')()),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('document_signed',
             self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'DocApproval', ['Contract'])

        # Deleting field 'Request.document'
        db.delete_column(u'DocApproval_request', 'document_id')

        # Adding field 'Request.contract'
        db.add_column(u'DocApproval_request', 'contract',
                      self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='contract',
                                                                               unique=True, null=True,
                                                                               to=orm['DocApproval.Contract']),
                      keep_default=False)

        # Adding field 'Request.updated'
        db.add_column(u'DocApproval_request', 'updated',
                      self.gf('django.db.models.fields.DateField')(auto_now=True,
                                                                   default=datetime.datetime(2013, 4, 29, 0, 0),
                                                                   blank=True),
                      keep_default=False)

        # Adding field 'Request.payed'
        db.add_column(u'DocApproval_request', 'payed',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.city'
        db.add_column(u'DocApproval_userprofile', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['DocApproval.City']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'DocApproval_document', (
            ('paid_date', self.gf('django.db.models.fields.DateField')()),
            ('contents_signed',
             self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('prolongation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active_period', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contents', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'DocApproval', ['Document'])

        # Deleting model 'Contract'
        db.delete_table(u'DocApproval_contract')

        # Adding field 'Request.document'
        db.add_column(u'DocApproval_request', 'document',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, related_name='document',
                                                                               unique=True, null=True,
                                                                               to=orm['DocApproval.Document'],
                                                                               blank=True),
                      keep_default=False)

        # Deleting field 'Request.contract'
        db.delete_column(u'DocApproval_request', 'contract_id')

        # Deleting field 'Request.updated'
        db.delete_column(u'DocApproval_request', 'updated')

        # Deleting field 'Request.payed'
        db.delete_column(u'DocApproval_request', 'payed')

        # Deleting field 'UserProfile.city'
        db.delete_column(u'DocApproval_userprofile', 'city_id')


    models = {
        u'DocApproval.city': {
            'Meta': {'object_name': 'City'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'DocApproval.contract': {
            'Meta': {'object_name': 'Contract'},
            'active_period': ('django.db.models.fields.IntegerField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'document_signed': (
                'django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_date': ('django.db.models.fields.DateField', [], {}),
            'prolongation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'DocApproval.dynamicsettings': {
            'Meta': {'object_name': 'DynamicSettings'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            'field_type': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'})
        },
        u'DocApproval.position': {
            'Meta': {'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        u'DocApproval.request': {
            'Meta': {'object_name': 'Request'},
            'accepted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.City']"}),
            'comments': (
                'django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.OneToOneField', [],
                         {'blank': 'True', 'related_name': "'contract'", 'unique': 'True', 'null': 'True',
                          'to': u"orm['DocApproval.Contract']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'created_by'", 'to': u"orm['DocApproval.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'payed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'send_on_approval': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.UserProfile']"}),
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
            'first_name_accusative': (
                'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'last_name_accusative': (
                'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [],
                        {'to': u"orm['DocApproval.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'middle_name_accusative': (
                'django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.Position']"}),
            'sign': (
                'django.db.models.fields.files.ImageField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [],
                     {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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

    complete_apps = ['DocApproval']