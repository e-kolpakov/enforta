# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'DepartmentCityOverride'
        db.create_table(u'DocApproval_departmentcityoverride', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.City'])),
            ('department', self.gf('django.db.models.fields.related.ForeignKey')(related_name='city_overrides',
                                                                                 to=orm['DocApproval.Department'])),
            ('show_in_list', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('responsible_user',
             self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DocApproval.UserProfile'], null=True,
                                                                   blank=True)),
        ))
        db.send_create_signal('DocApproval', ['DepartmentCityOverride'])

        # Adding unique constraint on 'DepartmentCityOverride', fields ['city', 'department']
        db.create_unique(u'DocApproval_departmentcityoverride', ['city_id', 'department_id'])

        # Deleting field 'Department.city'
        db.delete_column(u'DocApproval_department', 'city_id')


    def backwards(self, orm):
        # Removing unique constraint on 'DepartmentCityOverride', fields ['city', 'department']
        db.delete_unique(u'DocApproval_departmentcityoverride', ['city_id', 'department_id'])

        # Deleting model 'DepartmentCityOverride'
        db.delete_table(u'DocApproval_departmentcityoverride')

        # Adding field 'Department.city'
        db.add_column(u'DocApproval_department', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['DocApproval.City']),
                      keep_default=False)


    models = {
        'DocApproval.approvalprocess': {
            'Meta': {'object_name': 'ApprovalProcess'},
            'attempt_number': ('django.db.models.fields.IntegerField', [], {}),
            'current_step_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'route': ('django.db.models.fields.related.ForeignKey', [],
                      {'related_name': "'processes'", 'to': "orm['DocApproval.ApprovalRoute']"})
        },
        'DocApproval.approvalprocessaction': {
            'Meta': {'object_name': 'ApprovalProcessAction'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'action_taken': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.UserProfile']"}),
            'comment': (
            'django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'actions'", 'to': "orm['DocApproval.ApprovalProcess']"}),
            'step': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.ApprovalRouteStep']"})
        },
        'DocApproval.approvalroute': {
            'Meta': {'object_name': 'ApprovalRoute'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '4000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'DocApproval.approvalroutestep': {
            'Meta': {'object_name': 'ApprovalRouteStep'},
            'approver': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'approval_steps'", 'null': 'True', 'to': "orm['DocApproval.UserProfile']"}),
            'calc_step': (
            'django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route': ('django.db.models.fields.related.ForeignKey', [],
                      {'related_name': "'steps'", 'to': "orm['DocApproval.ApprovalRoute']"}),
            'step_number': ('django.db.models.fields.IntegerField', [], {})
        },
        'DocApproval.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        'DocApproval.contract': {
            'Meta': {'object_name': 'Contract'},
            'activation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'active_period': ('django.db.models.fields.IntegerField', [], {}),
            'active_period_unit': ('django.db.models.fields.CharField', [], {'default': "'days'", 'max_length': '50'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.Currency']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'document': ('DocApproval.utilities.file_upload.ContentTypeRestrictedFileField', [], {'max_length': '100'}),
            'document_signed': ('DocApproval.utilities.file_upload.ContentTypeRestrictedFileField', [],
                                {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'prolongation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'DocApproval.currency': {
            'Meta': {'object_name': 'Currency'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'caption_plural': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'short_caption': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'DocApproval.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'responsible_user': ('django.db.models.fields.related.ForeignKey', [],
                                 {'to': "orm['DocApproval.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'show_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'DocApproval.departmentcityoverride': {
            'Meta': {'unique_together': "(('city', 'department'),)", 'object_name': 'DepartmentCityOverride'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.City']"}),
            'department': ('django.db.models.fields.related.ForeignKey', [],
                           {'related_name': "'city_overrides'", 'to': "orm['DocApproval.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responsible_user': ('django.db.models.fields.related.ForeignKey', [],
                                 {'to': "orm['DocApproval.UserProfile']", 'null': 'True', 'blank': 'True'}),
            'show_in_list': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'DocApproval.position': {
            'Meta': {'object_name': 'Position'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_name': ('django.db.models.fields.CharField', [], {'max_length': '4000'})
        },
        'DocApproval.request': {
            'Meta': {'object_name': 'Request'},
            'accepted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'approval_route': ('django.db.models.fields.related.OneToOneField', [],
                               {'to': "orm['DocApproval.ApprovalRoute']", 'unique': 'True', 'null': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.City']"}),
            'comments': (
            'django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True', 'blank': 'True'}),
            'contract': ('django.db.models.fields.related.OneToOneField', [],
                         {'related_name': "'request'", 'unique': 'True', 'to': "orm['DocApproval.Contract']"}),
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'requests'", 'to': "orm['DocApproval.UserProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updater': ('django.db.models.fields.related.ForeignKey', [],
                             {'related_name': "'requests_last_updated_by'", 'to': "orm['DocApproval.UserProfile']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'send_on_approval': ('django.db.models.fields.related.ForeignKey', [],
                                 {'related_name': "'requests_to_be_sent_on_approval'",
                                  'to': "orm['DocApproval.UserProfile']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.RequestStatus']"}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'DocApproval.requesthistory': {
            'Meta': {'object_name': 'RequestHistory'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'action_parameters': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DocApproval.UserProfile']"}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '4000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'history'", 'to': "orm['DocApproval.Request']"})
        },
        'DocApproval.requeststatus': {
            'Meta': {'object_name': 'RequestStatus'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '800'})
        },
        'DocApproval.temporaryuserimpersonation': {
            'Meta': {'object_name': 'TemporaryUserImpersonation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_user': ('django.db.models.fields.related.ForeignKey', [],
                         {'related_name': "'replacing'", 'to': "orm['DocApproval.UserProfile']"}),
            'replaced_user': ('django.db.models.fields.related.ForeignKey', [],
                              {'related_name': "'replaced_by'", 'to': "orm['DocApproval.UserProfile']"}),
            'replacement_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'replacement_start': ('django.db.models.fields.DateField', [], {})
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