# encoding: utf-8
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.is_expertise'
        db.delete_column('project', 'is_expertise')

    def backwards(self, orm):
        # Adding field 'Project.is_expertise'
        db.add_column('project', 'is_expertise', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'machines.machinecategory': {
            'Meta': {'object_name': 'MachineCategory', 'db_table': "'machine_category'"},
            'datastore': ('django.db.models.fields.CharField', [], {'default': "'karaage.datastores.openldap_datastore'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'people.institute': {
            'Meta': {'object_name': 'Institute', 'db_table': "'institute'"},
            'delegates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'delegate'", 'to': "orm['people.Person']", 'through': "orm['people.InstituteDelegate']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'gid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'saml_entityid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'people.institutedelegate': {
            'Meta': {'object_name': 'InstituteDelegate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Institute']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'people.person': {
            'Meta': {'object_name': 'Person', 'db_table': "'person'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_approver'", 'null': 'True', 'to': "orm['people.Person']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_deletor'", 'null': 'True', 'to': "orm['people.Person']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Institute']"}),
            'is_systemuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_usage': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'saml_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'projects.project': {
            'Meta': {'object_name': 'Project', 'db_table': "'project'"},
            'additional_req': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_approver'", 'null': 'True', 'to': "orm['people.Person']"}),
            'date_approved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_deletor'", 'null': 'True', 'to': "orm['people.Person']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Institute']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_usage': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'leaders': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'leaders'", 'symmetrical': 'False', 'to': "orm['people.Person']"}),
            'machine_categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'projects'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['machines.MachineCategory']"}),
            'machine_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['machines.MachineCategory']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['people.Person']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['projects']
