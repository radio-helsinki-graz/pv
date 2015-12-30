# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BroadcastFormat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('format', models.CharField(max_length=32, verbose_name='Format')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('color', models.CharField(default=b'#ffffff', max_length=7, verbose_name='Color')),
                ('text_color', models.CharField(default=b'#000000', max_length=7, verbose_name='Text color')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
            ],
            options={
                'ordering': ('format',),
                'verbose_name': 'Broadcast format',
                'verbose_name_plural': 'Broadcast formats',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='E-Mail', blank=True)),
                ('website', models.URLField(verbose_name='Website', blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
        ),
        migrations.CreateModel(
            name='MusicFocus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('focus', models.CharField(max_length=32, verbose_name='Focus')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('focus',),
                'verbose_name': 'Music focus',
                'verbose_name_plural': 'Music focus',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('content', tinymce.models.HTMLField(verbose_name='Content')),
                ('status', models.IntegerField(default=1, verbose_name='Status', choices=[(0, 'Cancellation'), (1, 'Recommendation'), (2, 'Repetition')])),
                ('cba_entry_id', models.IntegerField(null=True, verbose_name='CBA entry ID', blank=True)),
                ('start', models.DateTimeField(editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('timeslot',),
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='ProgramSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('byweekday', models.IntegerField(verbose_name='Weekday', choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('dstart', models.DateField(verbose_name='First date')),
                ('tstart', models.TimeField(verbose_name='Start time')),
                ('tend', models.TimeField(verbose_name='End time')),
                ('until', models.DateField(verbose_name='Last date')),
                ('is_repetition', models.BooleanField(default=False, verbose_name='Is repetition')),
                ('automation_id', models.IntegerField(blank=True, null=True, verbose_name='Automation ID', choices=[(52018, '926Hertz'), (52069, 'Abunda Lingva'), (52145, 'Aficionados on Air'), (52140, 'AFRICAN TIME'), (52015, 'Alo Cristina!'), (52193, 'Anarchistisches Radio'), (52097, 'Arbeitslosenstammtisch'), (52178, 'Arbeitslosenstammtisch (Wiederholung)'), (52124, 'artcore'), (52142, 'Audiotop'), (52019, 'AUS CHANGE'), (52000, 'Aus den freien Radios'), (52143, 'avant_jazz'), (52022, 'A_partment politi_X'), (52053, 'A_partment politi_X (Wiederholung)'), (52079, 'Barrikaden und Pfeffer'), (52162, 'Between the Jigs and the Reels'), (52211, 'Between the Jigs and the Reels'), (52154, 'Between The Lines'), (52131, 'bumbumtschak'), (52221, 'c/o'), (52222, 'c/o'), (52220, 'c/o'), (52020, 'c/o'), (52224, 'c/o (Wiederholung)'), (52225, 'c/o (Wiederholung)'), (52223, 'c/o (Wiederholung)'), (52059, 'c/o (Wiederholung)'), (52014, 'Cafe Manchester'), (52065, 'Champion Sound'), (52017, 'clash connect'), (52139, 'Club Station'), (52207, 'Das offene Wort'), (52226, 'Das rote Mikro'), (52122, 'Das rote Mikro'), (52218, 'Das rote Mikro'), (52219, 'Das rote Mikro'), (52233, 'Das rote Mikro (Wiederholung)'), (52229, 'Das rote Mikro (Wiederholung)'), (52227, 'Das rote Mikro (Wiederholung)'), (52232, 'Das rote Mikro (Wiederholung)'), (52165, 'Das wilde Denken'), (52234, 'Das wilde Denken (Wiederholung)'), (52007, 'Democracy Now!'), (52192, 'derive'), (52093, 'derive (Wiederholung)'), (52235, 'Deutsche Demokratische Populaermusik'), (52096, 'Die Neue Stadt'), (52125, 'Die Radiokometen - Wir sind Radio!'), (52182, 'Die Radiokometen - Wir sind Radio! (Wiederholung)'), (52208, 'Die Sendung mit der Katz'), (52239, 'Die Stadt der Zukunft - die Zukunft der Stadt'), (52177, 'disko404 radioshow'), (52185, 'disko404 radioshow (Wiederholung)'), (52166, 'Dream-Spotting'), (52054, 'Eigenklang'), (52200, 'Emigranti'), (52176, 'Emigranti (Wiederholung)'), (52141, 'Exquisite Corps'), (52203, 'Final Transmission'), (52195, 'fixe'), (52091, 'Fluxkompensator'), (52209, 'Fokus Bildung'), (52068, 'Fratls Forum'), (52086, 'freigangproduktionen'), (52046, 'freigangproduktionen (Wiederholung)'), (52197, 'fridayshow'), (52158, 'FROzine'), (52050, 'FROzine (Wiederholung 1)'), (52052, 'FROzine (Wiederholung 2)'), (52136, 'Fr\xfchst\xfcck ohne Illusionen'), (52231, 'Ganz bei Trost'), (52099, 'gender frequenz - sozialpolitisch, feministisch, unbeugsam!'), (52013, 'gender frequenz - sozialpolitisch, feministisch, unbeugsam! (Wiederholung)'), (52189, 'Graz Sozial'), (52048, 'Hannas bunte Kommode'), (52089, 'headroom'), (52070, 'Helga Maria - live line'), (52202, 'HelsinKIDS'), (52058, 'Hotel Passage'), (52119, 'In Graz Verstrickt'), (52181, 'In Graz Verstrickt (Wiederholung)'), (52100, 'Jackolope - Bearfish and Country-Music'), (52149, 'Jazz-News'), (52044, 'Jazzkartell'), (52160, 'Jazzkartell (Wiederholung)'), (52051, "Jester's Soundtracks"), (52201, 'Jeux On Air'), (52009, 'Just to get a Rap'), (52173, 'Klassik am Sonntag'), (52004, 'Klimanews'), (52212, 'Kultlabor'), (52137, 'KunstR\xe4ume'), (52049, "L'heure bleue"), (52072, 'lady music'), (52214, 'Lange Lieder'), (52010, 'literadio on air'), (52213, 'Literatursprechstunde'), (52066, 'M Punkt Klengele (oder) ekw14,90'), (52057, 'Martinland'), (52184, 'Martinland (Wiederholung)'), (52157, 'Megaphonuni'), (52183, 'Megaphonuni (Wiederholung)'), (52071, 'Mit den Ohren lesen und schreiben'), (52237, 'Mit den Ohren lesen und schreiben (Wiederholen)'), (52196, 'morgen'), (52094, 'Morgenrunde'), (52001, 'Musica Latinoamericana!'), (52132, 'Musica Latinoamericana! (Wiederholung)'), (52061, 'Natur im Aether'), (52153, 'Neue Literatur am Donnerstag'), (52187, 'Not only Latin'), (52188, 'Not only Latin (Wiederholung)'), (52191, 'NUOVA MUSICA INTERNZIONALE'), (52228, 'O94 Nachrichten'), (52204, 'Ohrenw\xe4rmer'), (52008, 'onda-info'), (52216, 'Oozing Music Show'), (52081, 'Probeb\xfchne'), (52028, 'Programmvorschau Dienstag Abend'), (52026, 'Programmvorschau Dienstag Fr\xfch'), (52027, 'Programmvorschau Dienstag Mittag'), (52034, 'Programmvorschau Donnerstag Abend'), (52032, 'Programmvorschau Donnerstag Fr\xfch'), (52033, 'Programmvorschau Donnerstag Mittag'), (52037, 'Programmvorschau Freitag Abend'), (52035, 'Programmvorschau Freitag Fr\xfch'), (52036, 'Programmvorschau Freitag Mittag'), (52031, 'Programmvorschau Mittwoch Abend'), (52029, 'Programmvorschau Mittwoch Fr\xfch'), (52030, 'Programmvorschau Mittwoch Mittag'), (52025, 'Programmvorschau Montag Abend'), (52023, 'Programmvorschau Montag Fr\xfch'), (52024, 'Programmvorschau Montag Mittag'), (52040, 'Programmvorschau Samstag Abend'), (52038, 'Programmvorschau Samstag Fr\xfch'), (52039, 'Programmvorschau Samstag Mittag'), (52043, 'Programmvorschau Sonntag Abend'), (52041, 'Programmvorschau Sonntag Fr\xfch'), (52042, 'Programmvorschau Sonntag Mittag'), (52021, 'Pura Vida Sounds'), (52064, 'Pythagoras oder die feste Winkelsumme des Lebens'), (52194, 'Pythagoras oder die feste Winkelsumme des Lebens (Wiederholung)'), (52016, 'Querbeet'), (52230, 'Radio Auslandsdienst'), (52127, 'Radio Lax'), (52199, 'Radio LoPas'), (52151, 'Radio Marmelade'), (52003, 'Radio Netwatcher'), (52063, 'radio radia - radiokunst zum selbsthineinh\xf6ren'), (52002, 'Radio Rinia'), (52047, 'Radio Stimme'), (52045, 'radio%attac'), (52174, 'radio%attac (Wiederholung)'), (52133, 'Radyo Mezopotamya'), (52130, 'raumfest'), (52175, 'raumfest (Wiederholung)'), (52215, 'Resonate Project'), (52150, 'Rivendell Test (\xd63 Simulator)'), (52210, 'Rocktime'), (52006, 'Romania astazi - Rum\xe4nien heute'), (52161, 'Saunafm'), (52164, "Scenesters' Special"), (52103, 'Sendeschiene1-01'), (52104, 'Sendeschiene1-02'), (52105, 'Sendeschiene1-03'), (52106, 'Sendeschiene1-04'), (52107, 'Sendeschiene1-05'), (52108, 'Sendeschiene1-06'), (52109, 'Sendeschiene1-07'), (52110, 'Sendeschiene1-08'), (52111, 'Sendeschiene1-09'), (52112, 'Sendeschiene1-10'), (52113, 'Sendeschiene2-01'), (52114, 'Sendeschiene2-02'), (52115, 'Sendeschiene2-03'), (52116, 'Sendeschiene2-04'), (52117, 'Sendeschiene2-05'), (52120, 'Sendeschiene2-06'), (52236, 'Sendung mit Akzent'), (52198, 'Sigs Seelenkiste'), (52073, 'Sondersendung 1'), (52074, 'Sondersendung 2'), (52075, 'Sondersendung 3'), (52076, 'Sondersendung 4'), (52077, 'Sondersendung 5'), (52163, 'songbirds'), (52055, 'SPACEfemFM'), (52092, 'SportLeit'), (52088, 'SportLeit (Wiederholung)'), (52123, 'Steinzeit'), (52238, 'Steinzeit (Wiederholung)'), (52067, 'Styrian Underground'), (52152, 'substral'), (52146, 'Substral (Wiederholung)'), (52085, 'Szenenwechsel'), (52148, 'Szenenwechsel (Wiederholung)'), (52169, 'Tagtraum/Nachtwache'), (52011, 'testsendung1'), (52012, 'testsendung2'), (52156, 'Theo Cola'), (52168, 'Theo Cola (Wiederholung)'), (52171, 'Tierrechtsradio'), (52056, 'Toningenieursforum'), (52005, 'Tonspur'), (52083, 'Tramina FM'), (52101, 'Transgenderradio'), (52159, 'Transgenderradio (Wiederholung)'), (52090, 'Unerh\xf6rt - Radio ohne Barrieren'), (52180, 'Unerh\xf6rt - Radio ohne Barrieren (Wiederholung)'), (52098, 'Ungarische Mosaiken'), (52147, 'Von Unten (Donnerstag)'), (52129, 'Von Unten (Donnerstag, Wiederholung 1)'), (52170, 'Von Unten (Donnerstag, Wiederholung 2)'), (52134, 'Von Unten (Mittwoch)'), (52082, 'Von Unten (Mittwoch, Wiederholung 1)'), (52128, 'Von Unten (Mittwoch, Wiederholung 2)'), (52060, 'Von Unten im Gespraech WH'), (52080, 'Von Unten im Gespr\xe4ch'), (52126, 'Von Unten im Gespr\xe4ch (Wiederholung)'), (52155, 'Werkskantine'), (52095, 'WERKSTATT KULTUR'), (52078, 'Women on Air presents: Globale Dialoge'), (52172, 'Women on Air presents: Globale Dialoge (Wiederholung)'), (52121, 'Zapatistas: Caminando preguntamos - Fragend schreiten wir voran'), (52206, 'Zapatistas: Caminando preguntamos - Fragend schreiten wir voran (Wiederholung)'), (52186, 'Zwischen Kl\xe4ngen')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('dstart', 'tstart'),
                'verbose_name': 'Program slot',
                'verbose_name_plural': 'Program slots',
            },
        ),
        migrations.CreateModel(
            name='RRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name='Name')),
                ('freq', models.IntegerField(verbose_name='Frequency', choices=[(1, 'Monthly'), (2, 'Weekly'), (3, 'Daily')])),
                ('interval', models.IntegerField(default=1, verbose_name='Interval')),
                ('bysetpos', models.IntegerField(blank=True, null=True, verbose_name='Set position', choices=[(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (5, 'Fifth'), (-1, 'Last')])),
                ('count', models.IntegerField(null=True, verbose_name='Count', blank=True)),
            ],
            options={
                'ordering': ('-freq', 'interval', 'bysetpos'),
                'verbose_name': 'Recurrence rule',
                'verbose_name_plural': 'Recurrence rules',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('slug', models.CharField(unique=True, max_length=255, verbose_name='Slug')),
                ('image', models.ImageField(upload_to=b'show_images', null=True, verbose_name='Image', blank=True)),
                ('image_enabled', models.BooleanField(default=True, verbose_name='show Image')),
                ('short_description', models.CharField(max_length=64, verbose_name='Short description')),
                ('description', tinymce.models.HTMLField(null=True, verbose_name='Description', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='E-Mail', blank=True)),
                ('website', models.URLField(null=True, verbose_name='Website', blank=True)),
                ('cba_series_id', models.IntegerField(null=True, verbose_name='CBA series ID', blank=True)),
                ('automation_id', models.IntegerField(blank=True, null=True, verbose_name='Automation ID', choices=[(52018, '926Hertz'), (52069, 'Abunda Lingva'), (52145, 'Aficionados on Air'), (52140, 'AFRICAN TIME'), (52015, 'Alo Cristina!'), (52193, 'Anarchistisches Radio'), (52097, 'Arbeitslosenstammtisch'), (52178, 'Arbeitslosenstammtisch (Wiederholung)'), (52124, 'artcore'), (52142, 'Audiotop'), (52019, 'AUS CHANGE'), (52000, 'Aus den freien Radios'), (52143, 'avant_jazz'), (52022, 'A_partment politi_X'), (52053, 'A_partment politi_X (Wiederholung)'), (52079, 'Barrikaden und Pfeffer'), (52162, 'Between the Jigs and the Reels'), (52211, 'Between the Jigs and the Reels'), (52154, 'Between The Lines'), (52131, 'bumbumtschak'), (52221, 'c/o'), (52222, 'c/o'), (52220, 'c/o'), (52020, 'c/o'), (52224, 'c/o (Wiederholung)'), (52225, 'c/o (Wiederholung)'), (52223, 'c/o (Wiederholung)'), (52059, 'c/o (Wiederholung)'), (52014, 'Cafe Manchester'), (52065, 'Champion Sound'), (52017, 'clash connect'), (52139, 'Club Station'), (52207, 'Das offene Wort'), (52226, 'Das rote Mikro'), (52122, 'Das rote Mikro'), (52218, 'Das rote Mikro'), (52219, 'Das rote Mikro'), (52233, 'Das rote Mikro (Wiederholung)'), (52229, 'Das rote Mikro (Wiederholung)'), (52227, 'Das rote Mikro (Wiederholung)'), (52232, 'Das rote Mikro (Wiederholung)'), (52165, 'Das wilde Denken'), (52234, 'Das wilde Denken (Wiederholung)'), (52007, 'Democracy Now!'), (52192, 'derive'), (52093, 'derive (Wiederholung)'), (52235, 'Deutsche Demokratische Populaermusik'), (52096, 'Die Neue Stadt'), (52125, 'Die Radiokometen - Wir sind Radio!'), (52182, 'Die Radiokometen - Wir sind Radio! (Wiederholung)'), (52208, 'Die Sendung mit der Katz'), (52239, 'Die Stadt der Zukunft - die Zukunft der Stadt'), (52177, 'disko404 radioshow'), (52185, 'disko404 radioshow (Wiederholung)'), (52166, 'Dream-Spotting'), (52054, 'Eigenklang'), (52200, 'Emigranti'), (52176, 'Emigranti (Wiederholung)'), (52141, 'Exquisite Corps'), (52203, 'Final Transmission'), (52195, 'fixe'), (52091, 'Fluxkompensator'), (52209, 'Fokus Bildung'), (52068, 'Fratls Forum'), (52086, 'freigangproduktionen'), (52046, 'freigangproduktionen (Wiederholung)'), (52197, 'fridayshow'), (52158, 'FROzine'), (52050, 'FROzine (Wiederholung 1)'), (52052, 'FROzine (Wiederholung 2)'), (52136, 'Fr\xfchst\xfcck ohne Illusionen'), (52231, 'Ganz bei Trost'), (52099, 'gender frequenz - sozialpolitisch, feministisch, unbeugsam!'), (52013, 'gender frequenz - sozialpolitisch, feministisch, unbeugsam! (Wiederholung)'), (52189, 'Graz Sozial'), (52048, 'Hannas bunte Kommode'), (52089, 'headroom'), (52070, 'Helga Maria - live line'), (52202, 'HelsinKIDS'), (52058, 'Hotel Passage'), (52119, 'In Graz Verstrickt'), (52181, 'In Graz Verstrickt (Wiederholung)'), (52100, 'Jackolope - Bearfish and Country-Music'), (52149, 'Jazz-News'), (52044, 'Jazzkartell'), (52160, 'Jazzkartell (Wiederholung)'), (52051, "Jester's Soundtracks"), (52201, 'Jeux On Air'), (52009, 'Just to get a Rap'), (52173, 'Klassik am Sonntag'), (52004, 'Klimanews'), (52212, 'Kultlabor'), (52137, 'KunstR\xe4ume'), (52049, "L'heure bleue"), (52072, 'lady music'), (52214, 'Lange Lieder'), (52010, 'literadio on air'), (52213, 'Literatursprechstunde'), (52066, 'M Punkt Klengele (oder) ekw14,90'), (52057, 'Martinland'), (52184, 'Martinland (Wiederholung)'), (52157, 'Megaphonuni'), (52183, 'Megaphonuni (Wiederholung)'), (52071, 'Mit den Ohren lesen und schreiben'), (52237, 'Mit den Ohren lesen und schreiben (Wiederholen)'), (52196, 'morgen'), (52094, 'Morgenrunde'), (52001, 'Musica Latinoamericana!'), (52132, 'Musica Latinoamericana! (Wiederholung)'), (52061, 'Natur im Aether'), (52153, 'Neue Literatur am Donnerstag'), (52187, 'Not only Latin'), (52188, 'Not only Latin (Wiederholung)'), (52191, 'NUOVA MUSICA INTERNZIONALE'), (52228, 'O94 Nachrichten'), (52204, 'Ohrenw\xe4rmer'), (52008, 'onda-info'), (52216, 'Oozing Music Show'), (52081, 'Probeb\xfchne'), (52028, 'Programmvorschau Dienstag Abend'), (52026, 'Programmvorschau Dienstag Fr\xfch'), (52027, 'Programmvorschau Dienstag Mittag'), (52034, 'Programmvorschau Donnerstag Abend'), (52032, 'Programmvorschau Donnerstag Fr\xfch'), (52033, 'Programmvorschau Donnerstag Mittag'), (52037, 'Programmvorschau Freitag Abend'), (52035, 'Programmvorschau Freitag Fr\xfch'), (52036, 'Programmvorschau Freitag Mittag'), (52031, 'Programmvorschau Mittwoch Abend'), (52029, 'Programmvorschau Mittwoch Fr\xfch'), (52030, 'Programmvorschau Mittwoch Mittag'), (52025, 'Programmvorschau Montag Abend'), (52023, 'Programmvorschau Montag Fr\xfch'), (52024, 'Programmvorschau Montag Mittag'), (52040, 'Programmvorschau Samstag Abend'), (52038, 'Programmvorschau Samstag Fr\xfch'), (52039, 'Programmvorschau Samstag Mittag'), (52043, 'Programmvorschau Sonntag Abend'), (52041, 'Programmvorschau Sonntag Fr\xfch'), (52042, 'Programmvorschau Sonntag Mittag'), (52021, 'Pura Vida Sounds'), (52064, 'Pythagoras oder die feste Winkelsumme des Lebens'), (52194, 'Pythagoras oder die feste Winkelsumme des Lebens (Wiederholung)'), (52016, 'Querbeet'), (52230, 'Radio Auslandsdienst'), (52127, 'Radio Lax'), (52199, 'Radio LoPas'), (52151, 'Radio Marmelade'), (52003, 'Radio Netwatcher'), (52063, 'radio radia - radiokunst zum selbsthineinh\xf6ren'), (52002, 'Radio Rinia'), (52047, 'Radio Stimme'), (52045, 'radio%attac'), (52174, 'radio%attac (Wiederholung)'), (52133, 'Radyo Mezopotamya'), (52130, 'raumfest'), (52175, 'raumfest (Wiederholung)'), (52215, 'Resonate Project'), (52150, 'Rivendell Test (\xd63 Simulator)'), (52210, 'Rocktime'), (52006, 'Romania astazi - Rum\xe4nien heute'), (52161, 'Saunafm'), (52164, "Scenesters' Special"), (52103, 'Sendeschiene1-01'), (52104, 'Sendeschiene1-02'), (52105, 'Sendeschiene1-03'), (52106, 'Sendeschiene1-04'), (52107, 'Sendeschiene1-05'), (52108, 'Sendeschiene1-06'), (52109, 'Sendeschiene1-07'), (52110, 'Sendeschiene1-08'), (52111, 'Sendeschiene1-09'), (52112, 'Sendeschiene1-10'), (52113, 'Sendeschiene2-01'), (52114, 'Sendeschiene2-02'), (52115, 'Sendeschiene2-03'), (52116, 'Sendeschiene2-04'), (52117, 'Sendeschiene2-05'), (52120, 'Sendeschiene2-06'), (52236, 'Sendung mit Akzent'), (52198, 'Sigs Seelenkiste'), (52073, 'Sondersendung 1'), (52074, 'Sondersendung 2'), (52075, 'Sondersendung 3'), (52076, 'Sondersendung 4'), (52077, 'Sondersendung 5'), (52163, 'songbirds'), (52055, 'SPACEfemFM'), (52092, 'SportLeit'), (52088, 'SportLeit (Wiederholung)'), (52123, 'Steinzeit'), (52238, 'Steinzeit (Wiederholung)'), (52067, 'Styrian Underground'), (52152, 'substral'), (52146, 'Substral (Wiederholung)'), (52085, 'Szenenwechsel'), (52148, 'Szenenwechsel (Wiederholung)'), (52169, 'Tagtraum/Nachtwache'), (52011, 'testsendung1'), (52012, 'testsendung2'), (52156, 'Theo Cola'), (52168, 'Theo Cola (Wiederholung)'), (52171, 'Tierrechtsradio'), (52056, 'Toningenieursforum'), (52005, 'Tonspur'), (52083, 'Tramina FM'), (52101, 'Transgenderradio'), (52159, 'Transgenderradio (Wiederholung)'), (52090, 'Unerh\xf6rt - Radio ohne Barrieren'), (52180, 'Unerh\xf6rt - Radio ohne Barrieren (Wiederholung)'), (52098, 'Ungarische Mosaiken'), (52147, 'Von Unten (Donnerstag)'), (52129, 'Von Unten (Donnerstag, Wiederholung 1)'), (52170, 'Von Unten (Donnerstag, Wiederholung 2)'), (52134, 'Von Unten (Mittwoch)'), (52082, 'Von Unten (Mittwoch, Wiederholung 1)'), (52128, 'Von Unten (Mittwoch, Wiederholung 2)'), (52060, 'Von Unten im Gespraech WH'), (52080, 'Von Unten im Gespr\xe4ch'), (52126, 'Von Unten im Gespr\xe4ch (Wiederholung)'), (52155, 'Werkskantine'), (52095, 'WERKSTATT KULTUR'), (52078, 'Women on Air presents: Globale Dialoge'), (52172, 'Women on Air presents: Globale Dialoge (Wiederholung)'), (52121, 'Zapatistas: Caminando preguntamos - Fragend schreiten wir voran'), (52206, 'Zapatistas: Caminando preguntamos - Fragend schreiten wir voran (Wiederholung)'), (52186, 'Zwischen Kl\xe4ngen')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('broadcastformat', models.ForeignKey(related_name='shows', verbose_name='Broadcast format', to='program.BroadcastFormat')),
                ('hosts', models.ManyToManyField(related_name='shows', verbose_name='Hosts', to='program.Host')),
                ('musicfocus', models.ManyToManyField(related_name='shows', verbose_name='Music focus', to='program.MusicFocus')),
                ('owners', models.ManyToManyField(related_name='shows', verbose_name='Owners', to=settings.AUTH_USER_MODEL)),
                ('predecessor', models.ForeignKey(related_name='successors', verbose_name='Predecessor', blank=True, to='program.Show', null=True)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name': 'Show',
                'verbose_name_plural': 'Shows',
            },
        ),
        migrations.CreateModel(
            name='ShowInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('information', models.CharField(max_length=32, verbose_name='Information')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('information',),
                'verbose_name': 'Show information',
                'verbose_name_plural': 'Show information',
            },
        ),
        migrations.CreateModel(
            name='ShowTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('topic', models.CharField(max_length=32, verbose_name='Show topic')),
                ('abbrev', models.CharField(unique=True, max_length=4, verbose_name='Abbreviation')),
                ('slug', models.SlugField(unique=True, max_length=32, verbose_name='Slug')),
                ('button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image', blank=True)),
                ('button_hover', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Button image (hover)', blank=True)),
                ('big_button', models.ImageField(upload_to=b'buttons', null=True, verbose_name='Big button image', blank=True)),
            ],
            options={
                'ordering': ('topic',),
                'verbose_name': 'Show topic',
                'verbose_name_plural': 'Show topics',
            },
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(unique=True, verbose_name='Start time')),
                ('end', models.DateTimeField(verbose_name='End time')),
                ('programslot', models.ForeignKey(related_name='timeslots', verbose_name='Program slot', to='program.ProgramSlot')),
                ('show', models.ForeignKey(related_name='timeslots', editable=False, to='program.Show')),
            ],
            options={
                'ordering': ('start', 'end'),
                'verbose_name': 'Time slot',
                'verbose_name_plural': 'Time slots',
            },
        ),
        migrations.AddField(
            model_name='show',
            name='showinformation',
            field=models.ManyToManyField(related_name='shows', verbose_name='Show information', to='program.ShowInformation'),
        ),
        migrations.AddField(
            model_name='show',
            name='showtopic',
            field=models.ManyToManyField(related_name='shows', verbose_name='Show topic', to='program.ShowTopic'),
        ),
        migrations.AddField(
            model_name='programslot',
            name='rrule',
            field=models.ForeignKey(related_name='programslots', verbose_name='Recurrence rule', to='program.RRule'),
        ),
        migrations.AddField(
            model_name='programslot',
            name='show',
            field=models.ForeignKey(related_name='programslots', verbose_name='Show', to='program.Show'),
        ),
        migrations.AddField(
            model_name='note',
            name='show',
            field=models.ForeignKey(related_name='notes', editable=False, to='program.Show'),
        ),
        migrations.AddField(
            model_name='note',
            name='timeslot',
            field=models.OneToOneField(verbose_name='Time slot', to='program.TimeSlot'),
        ),
        migrations.AlterUniqueTogether(
            name='programslot',
            unique_together=set([('rrule', 'byweekday', 'dstart', 'tstart')]),
        ),
    ]
