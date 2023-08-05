# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import connection


class Migration(SchemaMigration):

    # Migrations that must run *after* we update the person model and remove the
    # user FK.
    needed_by = (
        ('machines', '0013_nop'),
        ('projects', '0010_auto'),
        ('institutes', '0006_auto__chg_field_institutechunk_institute'),
        ('software', '0009_nop'),
        ('common', '0002_move_comments'),
        ('applications', '0019_auto__add_field_applicant_short_name__add_field_applicant_full_name'),
    )

    def forwards(self, orm):
        cursor = connection.cursor()
        django_comments_exists = ('django_comments' in
                                  connection.introspection.get_table_list(cursor))
        django_comment_flags_exists = ('django_comment_flags' in
                                       connection.introspection.get_table_list(cursor))

        db.alter_column(
            'django_admin_log', 'person_id',
            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person']))

        if django_comments_exists:
            db.alter_column('django_comments', 'person_id',
                            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person']))
        if django_comment_flags_exists:
            db.alter_column('django_comment_flags', 'person_id',
                            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person']))

        db.delete_column('django_admin_log', 'user_id')
        if django_comments_exists:
            db.delete_column('django_comments', 'user_id')
        if django_comment_flags_exists:
            db.delete_column('django_comment_flags', 'user_id')

        db.rename_column('django_admin_log', 'person_id', 'user_id')
        if django_comments_exists:
            db.rename_column('django_comments', 'person_id', 'user_id')
        if django_comment_flags_exists:
            db.rename_column('django_comment_flags', 'person_id', 'user_id')

        # Deleting field 'Person.user'
        db.delete_column('person', 'user_id')

        # Changing field 'Person.username'
        db.alter_column('person', 'username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30))

        # Changing field 'Person.full_name'
        db.alter_column('person', 'full_name', self.gf('django.db.models.fields.CharField')(max_length=60))

        # Changing field 'Person.short_name'
        db.alter_column('person', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=30))

    def backwards(self, orm):
        cursor = connection.cursor()
        django_comments_exists = ('django_comments' in
                                  connection.introspection.get_table_list(cursor))
        django_comment_flags_exists = ('django_comment_flags' in
                                       connection.introspection.get_table_list(cursor))

        db.rename_column('django_admin_log', 'user_id', 'person_id')
        if django_comments_exists:
            db.rename_column('django_comments', 'user_id', 'person_id')
        if django_comment_flags_exists:
            db.rename_column('django_comment_flags', 'user_id', 'person_id')

        db.add_column('django_admin_log', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                      keep_default=False)
        if django_comments_exists:
            db.add_column('django_comments', 'user',
                          self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                          keep_default=False)
        if django_comment_flags_exists:
            db.add_column('django_comment_flags', 'user',
                          self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']),
                          keep_default=False)

        db.alter_column(
            'django_admin_log', 'person_id',
            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person'], null=True))
        if django_comments_exists:
            db.alter_column('django_comments', 'person_id',
                            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person'], null=True))
        if django_comment_flags_exists:
            db.alter_column('django_comment_flags', 'person_id',
                            self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.person'], null=True))

        # Adding field 'Person.user'
        db.add_column('person', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True),
                      keep_default=False)

        # Changing field 'Person.username'
        db.alter_column('person', 'username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, null=True))

        # Changing field 'Person.full_name'
        db.alter_column('person', 'full_name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True))

        # Changing field 'Person.short_name'
        db.alter_column('person', 'short_name', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

    models = {
        'institutes.institute': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institute', 'db_table': "'institute'"},
            'delegates': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'delegate'", 'to': "orm['people.Person']", 'through': "orm['institutes.InstituteDelegate']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'saml_entityid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'institutes.institutedelegate': {
            'Meta': {'object_name': 'InstituteDelegate', 'db_table': "'institutedelegate'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institutes.Institute']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'send_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'people.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'groups'", 'symmetrical': 'False', 'to': "orm['people.Person']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'people.person': {
            'Meta': {'ordering': "['full_name', 'short_name']", 'object_name': 'Person', 'db_table': "'person'"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_approver'", 'null': 'True', 'to': "orm['people.Person']"}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_deleted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_deletor'", 'null': 'True', 'to': "orm['people.Person']"}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'db_index': 'True'}),
            'expires': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institutes.Institute']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_systemuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_usage': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'legacy_ldap_password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'login_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'saml_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['people']
