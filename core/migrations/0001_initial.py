# Generated by Django 2.2 on 2019-05-09 18:01

import core.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('table', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='EntityMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='core.App')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maps', to='core.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('field_type', models.CharField(choices=[(core.models.FIELD_TYPES('char'), 'char'), (core.models.FIELD_TYPES('bool'), 'bool'), (core.models.FIELD_TYPES('int'), 'int'), (core.models.FIELD_TYPES('dec'), 'dec')], max_length=4)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Migration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_executed', models.DateTimeField()),
                ('first', models.BooleanField(default=False)),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='migrations', to='core.Entity')),
            ],
        ),
        migrations.CreateModel(
            name='MappedField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(max_length=30)),
                ('entity_map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.EntityMap')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='core.Field')),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='migration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='core.Migration'),
        ),
        migrations.AddField(
            model_name='entity',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entities', to='core.Solution'),
        ),
        migrations.AddField(
            model_name='app',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apps', to='core.Solution'),
        ),

        migrations.RunSQL(
            'CREATE SCHEMA entities'
        ),

        migrations.RunSQL(
            'CREATE EXTENSION "uuid-ossp" WITH SCHEMA entities;'
        ),
        #uuid_generate_v4()
        migrations.RunSQL(
        """
            CREATE OR REPLACE FUNCTION entities.save_history()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $function$
                BEGIN

                    EXECUTE 'INSERT INTO entities.' || TG_RELID::regclass::text || '_history SELECT 1 as pk, ($1).*' USING OLD;
                    RETURN NEW;
                END;
            $function$
        """
        ),
    ]
