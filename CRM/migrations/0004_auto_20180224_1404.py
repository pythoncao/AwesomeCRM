# Generated by Django 2.0.1 on 2018-02-24 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRM', '0003_auto_20180211_0459'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.SmallIntegerField(choices=[(0, '报名费'), (1, '学费'), (2, '退费')], default=0)),
                ('amount', models.IntegerField(default=500, verbose_name='费用')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agreed', models.BooleanField(default=False)),
                ('contract_signed_date', models.DateTimeField(blank=True, null=True)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_approved_date', models.DateTimeField(blank=True, null=True, verbose_name='合同审核时间')),
                ('class_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.ClassList')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.UserProfile')),
            ],
        ),
        migrations.AlterModelOptions(
            name='customerinfo',
            options={'verbose_name': '客户信息', 'verbose_name_plural': '客户信息'},
        ),
        migrations.AlterField(
            model_name='student',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CRM.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRM.StudentEnrollment'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CRM.ContractTemplate'),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together={('customer', 'class_grade')},
        ),
    ]