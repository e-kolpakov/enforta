# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Position'
        db.create_table(u'DocApproval_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position_name', self.gf('django.db.models.fields.CharField')(max_length=4000)),
        ))
        db.send_create_signal(u'DocApproval', ['Position'])

        # Adding model 'City'
        db.create_table(u'DocApproval_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city_name', self.gf('django.db.models.fields.CharField')(max_length=4000)),
        ))
        db.send_create_signal(u'DocApproval', ['City'])

        # Adding model 'RequestStatus'
        db.create_table(u'DocApproval_requeststatus', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('status_name', self.gf('django.db.models.fields.CharField')(max_length=800)),
        ))
        db.send_create_signal(u'DocApproval', ['RequestStatus'])

        # Adding model 'DynamicSettings'
        db.create_table(u'DocApproval_dynamicsettings', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=800)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True)),
            ('field_type', self.gf('django.db.models.fields.IntegerField')()),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True)),
        ))
        db.send_create_signal(u'DocApproval', ['DynamicSettings'])

        # Adding model 'UserProfile'
        db.create_table(u'DocApproval_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True,
                                                                              primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('middle_name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('last_name_accusative',
             self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('first_name_accusative',
             self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('middle_name_accusative',
             self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('sign', self.gf('django.db.models.fields.files.ImageField')(max_length=800, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=800)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.Position'])),
            ('manager',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.UserProfile'], null=True,
                                                                   blank=True)),
        ))
        db.send_create_signal(u'DocApproval', ['UserProfile'])

        # Adding model 'Document'
        db.create_table(u'DocApproval_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('active_period', self.gf('django.db.models.fields.IntegerField')()),
            ('prolongation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_date', self.gf('django.db.models.fields.DateField')()),
            ('contents', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('contents_signed',
             self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'DocApproval', ['Document'])

        # Adding model 'Request'
        db.create_table(u'DocApproval_request', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=4000, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('accepted', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.City'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.RequestStatus'])),
            ('document',
             self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='document', unique=True,
                                                                      null=True, to=orm['DocApproval.Document'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_by',
                                                                              to=orm['DocApproval.UserProfile'])),
            ('send_on_approval',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.UserProfile'])),
        ))
        db.send_create_signal(u'DocApproval', ['Request'])


    def backwards(self, orm):
        # Deleting model 'Position'
        db.delete_table(u'DocApproval_position')

        # Deleting model 'City'
        db.delete_table(u'DocApproval_city')

        # Deleting model 'RequestStatus'
        db.delete_table(u'DocApproval_requeststatus')

        # Deleting model 'DynamicSettings'
        db.delete_table(u'DocApproval_dynamicsettings')

        # Deleting model 'UserProfile'
        db.delete_table(u'DocApproval_userprofile')

        # Deleting model 'Document'
        db.delete_table(u'DocApproval_document')

        # Deleting model 'Request'
        db.delete_table(u'DocApproval_request')


    models = {
        u'DocApproval.city': {
            'Meta': {'object_name': 'City'},
            'city_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'DocApproval.document': {
            'Meta': {'object_name': 'Document'},
            'active_period': ('django.db.models.fields.IntegerField', [], {}),
            'contents': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'contents_signed': (
                'django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
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
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'created_by'", 'to': u"orm['DocApproval.UserProfile']"}),
            'document': ('django.db.models.fields.related.OneToOneField', [],
                         {'blank': 'True', 'related_name': "'document'", 'unique': 'True', 'null': 'True',
                          'to': u"orm['DocApproval.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'send_on_approval': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.UserProfile']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['DocApproval.RequestStatus']"})
        },
        u'DocApproval.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'status_name': ('django.db.models.fields.CharField', [], {'max_length': '800'})
        },
        u'DocApproval.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
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