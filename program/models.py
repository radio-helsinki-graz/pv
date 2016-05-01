from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from tinymce import models as tinymce_models

from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule

from utils import get_automation_id_choices


class BroadcastFormat(models.Model):
    format = models.CharField(_("Format"), max_length=32)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)
    color = models.CharField(_("Color"), max_length=7, default='#ffffff')
    text_color = models.CharField(_("Text color"), max_length=7, default='#000000')
    enabled = models.BooleanField(_("Enabled"), default=True)

    class Meta:
        ordering = ('format',)
        verbose_name = _("Broadcast format")
        verbose_name_plural = _("Broadcast formats")

    def admin_color(self):
        return u'<span style="background-color: %s; color: %s; padding: 0.2em">%s/%s</span>' % (
            self.color, self.text_color, self.color, self.text_color)

    admin_color.short_description = _("Color")
    admin_color.allow_tags = True

    def __unicode__(self):
        return u'%s' % self.format


class ShowInformation(models.Model):
    information = models.CharField(_("Information"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)
    button = models.ImageField(_("Button image"), blank=True, null=True, upload_to='buttons')
    button_hover = models.ImageField(_("Button image (hover)"), blank=True, null=True, upload_to='buttons')
    big_button = models.ImageField(_("Big button image"), blank=True, null=True, upload_to='buttons')

    class Meta:
        ordering = ('information',)
        verbose_name = _("Show information")
        verbose_name_plural = _("Show information")

    def admin_buttons(self):
        buttons = []
        if self.button:
            buttons.append(u'<img src="%s" />' % self.button.url)
        else:
            buttons.append(u'x')

        if self.button_hover:
            buttons.append(u'<img src="%s" />' % self.button_hover.url)
        else:
            buttons.append(u'x')

        if self.big_button:
            buttons.append(u'<img src="%s" />' % self.big_button.url)
        else:
            buttons.append(u'x')

        return ' '.join(buttons)

    admin_buttons.short_description = _("Buttons")
    admin_buttons.allow_tags = True

    def button_url(self):
        if self.button:
            return self.button.url
        else:
            return '/site_media/buttons/default-11.png'

    def button_hover_url(self):
        if self.button_hover:
            return self.button_hover.url
        else:
            return '/site_media/buttons/default-11.png'

    def big_button_url(self):
        if self.big_button:
            return self.big_button.url
        else:
            return '/site_media/buttons/default-17.png'

    def __unicode__(self):
        return u'%s' % self.information


class ShowTopic(models.Model):
    topic = models.CharField(_("Show topic"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)
    button = models.ImageField(_("Button image"), blank=True, null=True, upload_to='buttons')
    button_hover = models.ImageField(_("Button image (hover)"), blank=True, null=True, upload_to='buttons')
    big_button = models.ImageField(_("Big button image"), blank=True, null=True, upload_to='buttons')

    class Meta:
        ordering = ('topic',)
        verbose_name = _("Show topic")
        verbose_name_plural = _("Show topics")

    def admin_buttons(self):
        buttons = []
        if self.button:
            buttons.append(u'<img src="%s" />' % self.button.url)
        else:
            buttons.append(u'x')

        if self.button_hover:
            buttons.append(u'<img src="%s" />' % self.button_hover.url)
        else:
            buttons.append(u'x')

        if self.big_button:
            buttons.append(u'<img src="%s" />' % self.big_button.url)
        else:
            buttons.append(u'x')

        return ' '.join(buttons)

    admin_buttons.short_description = _("Buttons")
    admin_buttons.allow_tags = True

    def button_url(self):
        if self.button:
            return self.button.url
        else:
            return '/site_media/buttons/default-11.png'

    def button_hover_url(self):
        if self.button_hover:
            return self.button_hover.url
        else:
            return '/site_media/buttons/default-11.png'

    def big_button_url(self):
        if self.big_button:
            return self.big_button.url
        else:
            return '/site_media/buttons/default-17.png'

    def __unicode__(self):
        return u'%s' % self.topic


class MusicFocus(models.Model):
    focus = models.CharField(_("Focus"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)
    button = models.ImageField(_("Button image"), blank=True, null=True, upload_to='buttons')
    button_hover = models.ImageField(_("Button image (hover)"), blank=True, null=True, upload_to='buttons')
    big_button = models.ImageField(_("Big button image"), blank=True, null=True, upload_to='buttons')

    class Meta:
        ordering = ('focus',)
        verbose_name = _("Music focus")
        verbose_name_plural = _("Music focus")

    def admin_buttons(self):
        buttons = []
        if self.button:
            buttons.append(u'<img src="%s" />' % self.button.url)
        else:
            buttons.append(u'x')

        if self.button_hover:
            buttons.append(u'<img src="%s" />' % self.button_hover.url)
        else:
            buttons.append(u'x')

        if self.big_button:
            buttons.append(u'<img src="%s" />' % self.big_button.url)
        else:
            buttons.append(u'x')

        return ' '.join(buttons)

    admin_buttons.short_description = _("Buttons")
    admin_buttons.allow_tags = True

    def button_url(self):
        if self.button:
            return self.button.url
        else:
            return '/site_media/buttons/default-11.png'

    def button_hover_url(self):
        if self.button_hover:
            return self.button_hover.url
        else:
            return '/site_media/buttons/default-11.png'

    def big_button_url(self):
        if self.big_button:
            return self.big_button.url
        else:
            return '/site_media/buttons/default-17.png'

    def __unicode__(self):
        return u'%s' % self.focus


class Host(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    is_always_visible = models.BooleanField(_("Is always visible"), default=False)
    is_active = models.BooleanField(_("Is active"), default=True, editable=False)
    email = models.EmailField(_("E-Mail"), blank=True)
    website = models.URLField(_("Website"), blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Host")
        verbose_name_plural = _("Hosts")

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('host-detail', args=[str(self.id)])


class Show(models.Model):
    predecessor = models.ForeignKey('self', blank=True, null=True, related_name='successors', verbose_name=_("Predecessor"))
    hosts = models.ManyToManyField(Host, blank=True, related_name='shows', verbose_name=_("Hosts"))
    owners = models.ManyToManyField(User, blank=True, related_name='shows', verbose_name=_("Owners"))
    broadcastformat = models.ForeignKey(BroadcastFormat, related_name='shows', verbose_name=_("Broadcast format"))
    showinformation = models.ManyToManyField(ShowInformation, blank=True, related_name='shows', verbose_name=_("Show information"))
    showtopic = models.ManyToManyField(ShowTopic, blank=True, related_name='shows', verbose_name=_("Show topic"))
    musicfocus = models.ManyToManyField(MusicFocus, blank=True, related_name='shows', verbose_name=_("Music focus"))
    name = models.CharField(_("Name"), max_length=255)
    slug = models.CharField(_("Slug"), max_length=255, unique=True)
    image = models.ImageField(_("Image"), blank=True, null=True, upload_to='show_images')
    image_enabled = models.BooleanField(_("show Image"), default=True)
    short_description = models.CharField(_("Short description"), max_length=64)
    description = tinymce_models.HTMLField(_("Description"), blank=True, null=True)
    email = models.EmailField(_("E-Mail"), blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    is_active = models.BooleanField(_("Is active"), default=True, editable=False)
    cba_series_id = models.IntegerField(_("CBA series ID"), blank=True, null=True)
    automation_id = models.IntegerField(_("Automation ID"), blank=True, null=True, choices=get_automation_id_choices())
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('slug',)
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        return reverse('show-detail', args=[self.slug])


class RRule(models.Model):
    FREQ_CHOICES = (
        (1, _("Monthly")),
        (2, _("Weekly")),
        (3, _("Daily")),
    )
    BYSETPOS_CHOICES = (
        (1, _("First")),
        (2, _("Second")),
        (3, _("Third")),
        (4, _("Fourth")),
        (5, _("Fifth")),
        (-1, _("Last")),
    )
    name = models.CharField(_("Name"), max_length=32, unique=True)
    freq = models.IntegerField(_("Frequency"), choices=FREQ_CHOICES)
    interval = models.IntegerField(_("Interval"), default=1)
    bysetpos = models.IntegerField(_("Set position"), blank=True,
                                   choices=BYSETPOS_CHOICES, null=True)
    count = models.IntegerField(_("Count"), blank=True, null=True)

    class Meta:
        ordering = ('-freq', 'interval', 'bysetpos')
        verbose_name = _("Recurrence rule")
        verbose_name_plural = _("Recurrence rules")

    def __unicode__(self):
        return u'%s' % self.name


class ProgramSlot(models.Model):
    BYWEEKDAY_CHOICES = (
        (0, _("Monday")),
        (1, _("Tuesday")),
        (2, _("Wednesday")),
        (3, _("Thursday")),
        (4, _("Friday")),
        (5, _("Saturday")),
        (6, _("Sunday")),
    )
    rrule = models.ForeignKey(RRule, related_name='programslots', verbose_name=_("Recurrence rule"))
    byweekday = models.IntegerField(_("Weekday"), choices=BYWEEKDAY_CHOICES)
    show = models.ForeignKey(Show, related_name='programslots', verbose_name=_("Show"))
    dstart = models.DateField(_("First date"))
    tstart = models.TimeField(_("Start time"))
    tend = models.TimeField(_("End time"))
    until = models.DateField(_("Last date"))
    is_active = models.BooleanField(_("Is active"), default=True, editable=False)
    is_repetition = models.BooleanField(_("Is repetition"), default=False)
    automation_id = models.IntegerField(_("Automation ID"), blank=True, null=True, choices=get_automation_id_choices())
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('dstart', 'tstart')
        unique_together = ('rrule', 'byweekday', 'dstart', 'tstart')
        verbose_name = _("Program slot")
        verbose_name_plural = _("Program slots")

    def __unicode__(self):
        weekday = self.BYWEEKDAY_CHOICES[self.byweekday][1]
        tend = self.tend.strftime('%H:%M')
        dstart = self.dstart.strftime('%d. %b %Y')
        tstart = self.tstart.strftime('%H:%M')

        if self.rrule.freq == 0:
            return u'%s, %s - %s' % (dstart, tstart, tend)
        if self.rrule.freq == 3:
            return u'%s, %s - %s' % (self.rrule, tstart, tend)
        else:
            return u'%s, %s, %s - %s' % (weekday, self.rrule, tstart, tend)

    def save(self, *args, **kwargs):
        if self.pk:
            old = ProgramSlot.objects.get(pk=self.pk)
            if self.rrule != old.rrule:
                raise ValidationError(u"Recurrence rule cannot ba changed")
            if self.byweekday != old.byweekday:
                raise ValidationError(u"Weekday cannot be changed")
            if self.show != old.show:
                raise ValidationError(u"Show cannot be changed")
            if self.dstart != old.dstart:
                raise ValidationError(u"First date cannot ba changed")
            if self.tstart != old.tstart:
                raise ValidationError(u"Start time cannot be changed")
            if self.tend != old.tend:
                raise ValidationError(u"End time cannot be changed")
            if self.is_repetition != old.is_repetition:
                raise ValidationError(u"Is repetition cannot be changed")
        else:
            old = False

        self.is_active = self.until > date.today()
        self.show.is_active = self.until > date.today()

        super(ProgramSlot, self).save(*args, **kwargs)

        if self.rrule.freq == 0:
            byweekday_start = None
            byweekday_end = None
        elif self.rrule.freq == 3:
            byweekday_start = (0, 1, 2, 3, 4, 5, 6)
            byweekday_end = (0, 1, 2, 3, 4, 5, 6)
        else:
            byweekday_start = int(self.byweekday)

            if self.tend < self.tstart:
                if self.byweekday < 6:
                    byweekday_end = int(self.byweekday + 1)
                else:
                    byweekday_end = 0
            else:
                byweekday_end = int(self.byweekday)

        if self.tend < self.tstart:
            dend = self.dstart + timedelta(days=+1)
        else:
            dend = self.dstart

        starts = list(rrule(freq=self.rrule.freq,
                            dtstart=datetime.combine(self.dstart, self.tstart),
                            interval=self.rrule.interval,
                            until=self.until + relativedelta(days=+1),
                            bysetpos=self.rrule.bysetpos,
                            byweekday=byweekday_start))
        ends = list(rrule(freq=self.rrule.freq,
                          dtstart=datetime.combine(dend, self.tend),
                          interval=self.rrule.interval,
                          until=self.until + relativedelta(days=+1),
                          bysetpos=self.rrule.bysetpos,
                          byweekday=byweekday_end))

        if not old:
            for k in range(min(len(starts), len(ends))):
                TimeSlot.objects.create(programslot=self, start=starts[k], end=ends[k])
        elif self.until > old.until:
            for k in range(min(len(starts), len(ends))):
                if starts[k].date() > old.until:
                    TimeSlot.objects.create(programslot=self, start=starts[k], end=ends[k])


class TimeSlotManager(models.Manager):
    @staticmethod
    def get_or_create_current():
        try:
            return TimeSlot.objects.get(start__lte=datetime.now(), end__gt=datetime.now())
        except MultipleObjectsReturned:
            return TimeSlot.objects.filter(start__lte=datetime.now(), end__gt=datetime.now())[0]
        except ObjectDoesNotExist:
            once = RRule.objects.get(pk=1)
            today = date.today().weekday()
            default = Show.objects.get(pk=1)

            previous_timeslot = TimeSlot.objects.filter(end__lte=datetime.now()).order_by('-start')[0]
            next_timeslot = TimeSlot.objects.filter(start__gte=datetime.now())[0]

            dstart, tstart = previous_timeslot.end.date(), previous_timeslot.end.time()
            until, tend = next_timeslot.start.date(), next_timeslot.start.time()

            new_programslot = ProgramSlot(rrule=once,
                                          byweekday=today,
                                          show=default,
                                          dstart=dstart,
                                          tstart=tstart,
                                          tend=tend,
                                          until=until)

            try:
                new_programslot.validate_unique()
                new_programslot.save()
            except ValidationError:
                pass
            else:
                return new_programslot.timeslots.all()[0]

    @staticmethod
    def get_day_timeslots(day):
        today = datetime.combine(day, time(6, 0))
        tomorrow = today + timedelta(days=1)

        return TimeSlot.objects.filter(Q(start__lte=today, end__gte=today) |
                                       Q(start__gt=today, start__lt=tomorrow)).exclude(end=today)

    @staticmethod
    def get_24h_timeslots(start):
        end = start + timedelta(hours=24)

        return TimeSlot.objects.filter(Q(start__lte=start, end__gte=start) |
                                       Q(start__gt=start, start__lt=end)).exclude(end=start)


class TimeSlot(models.Model):
    programslot = models.ForeignKey(ProgramSlot, related_name='timeslots', verbose_name=_("Program slot"))
    start = models.DateTimeField(_("Start time"), unique=True)
    end = models.DateTimeField(_("End time"))
    show = models.ForeignKey(Show, editable=False, related_name='timeslots')

    objects = TimeSlotManager()

    class Meta:
        ordering = ('start', 'end')
        verbose_name = _("Time slot")
        verbose_name_plural = _("Time slots")

    def __unicode__(self):
        start = self.start.strftime('%d. %b %Y %H:%M')
        end = self.end.strftime('%H:%M')

        return u'%s: %s - %s' % (self.show, start, end)

    def save(self, *args, **kwargs):
        self.show = self.programslot.show
        super(TimeSlot, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('timeslot-detail', args=[str(self.id)])


class Note(models.Model):
    STATUS_CHOICES = (
        (0, _("Cancellation")),
        (1, _("Recommendation")),
        (2, _("Repetition")),
    )
    timeslot = models.OneToOneField(TimeSlot, verbose_name=_("Time slot"))
    title = models.CharField(_("Title"), max_length=128)
    content = tinymce_models.HTMLField(_("Content"))
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, default=1)
    cba_entry_id = models.IntegerField(_("CBA entry ID"), blank=True, null=True)
    start = models.DateTimeField(editable=False)
    show = models.ForeignKey(Show, editable=False, related_name='notes')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('timeslot',)
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.timeslot)

    def save(self, *args, **kwargs):
        self.start = self.timeslot.start
        self.show = self.timeslot.programslot.show

        super(Note, self).save(*args, **kwargs)
