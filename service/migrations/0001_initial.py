# Generated by Django 4.2 on 2024-02-28 16:24

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, help_text='Номер счета (для чековых начинается с символов “101-“, для сберегательных – с символов “102-”)', max_length=100, unique=True, verbose_name='Номер счета')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Баланс')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_debtor', models.BooleanField(default=False, verbose_name='Статус должника')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='client_groups', related_query_name='client', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='client_user_permissions', related_query_name='client', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ListAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.account')),
            ],
        ),
        migrations.CreateModel(
            name='TypeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('physical', 'Физическое лицо'), ('legal', 'Юридическое лицо')], max_length=100, verbose_name='Тип пользователя')),
            ],
        ),
        migrations.CreateModel(
            name='TypeListUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.typeuser', verbose_name='Тип пользователя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='typelistuser', to='service.client')),
            ],
        ),
        migrations.CreateModel(
            name='PhisycalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('firstname', models.CharField(max_length=100, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=100, verbose_name='Отчество')),
                ('birth_day', models.DateField(verbose_name='Дата рождения')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес прописки')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Номер телефона')),
                ('gender', models.CharField(choices=[('man', 'М'), ('woman', 'Ж')], max_length=5, verbose_name='Пол')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Аватар')),
                ('is_stuff', models.BooleanField(default=False, verbose_name='Сотрудник банка')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='physicalusers', to='service.client')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_code', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Код транзакции')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('is_paid_for', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('list_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_account', to='service.listaccount')),
            ],
        ),
        migrations.AddField(
            model_name='listaccount',
            name='type_list_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_list_user_account', to='service.typelistuser'),
        ),
        migrations.CreateModel(
            name='LegalUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_name', models.CharField(max_length=100, verbose_name='Название организации')),
                ('address', models.CharField(max_length=100, verbose_name='Адрес организации')),
                ('boss_full_name', models.CharField(max_length=100, verbose_name='ФИО директора')),
                ('accountant_full_name', models.CharField(max_length=100, verbose_name='ФИО главного бухгалтера')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Контактный номер')),
                ('form_of_ownership', models.CharField(choices=[('public', 'Государственная'), ('private', 'Частная'), ('foreign enterprise', 'Иностранное предприятие'), ('mixed', 'Смешанная')], max_length=100, verbose_name='Форма организации')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legalusers', to='service.client')),
            ],
        ),
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Тип карты')),
                ('account_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.accounttype')),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='service.accounttype'),
        ),
    ]
