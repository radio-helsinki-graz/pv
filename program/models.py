from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule

class BroadcastFormat(models.Model):
    format = models.CharField(_("Format"), max_length=32)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)

    class Meta:
        ordering = ('format',)
        verbose_name = _("Broadcast format")
        verbose_name_plural = _("Broadcast formats")

    def __unicode__(self):
        return u'%s' % self.format

class ShowInformation(models.Model):
    information = models.CharField(_("Information"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)

    class Meta:
        ordering = ('information',)
        verbose_name = _("Show information")
        verbose_name_plural = _("Show information")

    def __unicode__(self):
        return u'%s' % self.information

class ShowTopic(models.Model):
    topic = models.CharField(_("Show topic"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)

    class Meta:
        ordering = ('topic',)
        verbose_name = _("Show topic")
        verbose_name_plural = _("Show topics")

    def __unicode__(self):
        return u'%s' % self.topic

class MusicFocus(models.Model):
    focus = models.CharField(_("Focus"), max_length=32)
    abbrev = models.CharField(_("Abbreviation"), max_length=4, unique=True)
    slug = models.SlugField(_("Slug"), max_length=32, unique=True)

    class Meta:
        ordering = ('focus',)
        verbose_name = _("Music focus")
        verbose_name_plural = _("Music focus")

    def __unicode__(self):
        return u'%s' % self.focus

class Host(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    email = models.EmailField(_("E-Mail"), blank=True)
    website = models.URLField(_("Website"), blank=True)

    class Meta:
         ordering = ('name',)
         verbose_name = _("Host")
         verbose_name_plural = _("Hosts")

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('host-detail', [str(self.id)])

class Show(models.Model):
    predecessor = models.ForeignKey('self', blank=True, null=True, related_name='successors', verbose_name=_("Predecessor"))
    hosts = models.ManyToManyField(Host, blank=True, null=True, related_name='shows', verbose_name=_("Hosts"))
    owners = models.ManyToManyField(User, blank=True, null=True, related_name='shows', verbose_name=_("Owners"))
    broadcastformat = models.ForeignKey(BroadcastFormat, related_name='shows', verbose_name=_("Broadcast format"))
    showinformation = models.ManyToManyField(ShowInformation, blank=True, null=True, related_name='shows', verbose_name=_("Show information"))
    showtopic = models.ManyToManyField(ShowTopic, blank=True, null=True, related_name='shows', verbose_name=_("Show topic"))
    musicfocus = models.ManyToManyField(MusicFocus, blank=True, null=True, related_name='shows', verbose_name=_("Music focus"))
    name = models.CharField(_("Name"), max_length=256)
    slug = models.CharField(_("Slug"), max_length=255, unique=True)
    image = models.ImageField(_("Image"), blank=True, null=True, upload_to='show_images')
    short_description = models.CharField(_("Short description"), max_length=64)
    description = models.TextField(_("Description"))
    email = models.EmailField(_("E-Mail"), blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    cba_series_id = models.IntegerField(_("CBA series ID"), blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('slug',)
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        return ('show-detail', [self.slug])

    def has_active_programslots(self):
         return self.programslots.filter(until__gt=date.today()).count() > 0
    has_active_programslots.boolean = True
    has_active_programslots.short_description = _("Has active program slots")

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
    bysetpos = models.IntegerField(_("Set position"), blank=True, choices=BYSETPOS_CHOICES, null=True)
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
    is_repetition = models.BooleanField(_("Is repetition"), default=False)
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
        if not self.pk:
            super(ProgramSlot, self).save(*args, **kwargs)

            if self.rrule.freq == 0:
                byweekday_start = None
                byweekday_end = None
            elif self.rrule.freq == 3:
                byweekday_start = (0, 1, 2, 3, 4, 5, 6)
                byweekday_end = (0, 1, 2, 3, 4, 5, 6)
            else:
                byweekday_start = self.byweekday

                if self.tend < self.tstart:
                    byweekday_end = self.byweekday + 1 if self.byweekday < 6 else 0
                else:
                    byweekday_end = self.byweekday

            starts = list(rrule(freq=self.rrule.freq,
                dtstart=datetime.combine(self.dstart, self.tstart),
                interval=self.rrule.interval,
                until=self.until+relativedelta(days=+1),
                bysetpos=self.rrule.bysetpos,
                byweekday=byweekday_start))
            ends = list(rrule(freq=self.rrule.freq,
                dtstart=datetime.combine(self.dstart, self.tend),
                interval=self.rrule.interval,
                until=self.until+relativedelta(days=+1),
                bysetpos=self.rrule.bysetpos,
                byweekday=byweekday_end))

            for k in range(len(starts)):
                timeslot = TimeSlot(programslot=self, start=starts[k], end=ends[k])
                timeslot.save()

    def timeslot_count(self):
        return self.timeslots.count()
    timeslot_count.description = _("Time slot count")

class TimeSlotManager(models.Manager):
    def get_or_create_current(self):
        try:
            return TimeSlot.objects.get(start__lte=datetime.now(), end__gt=datetime.now())
        except ObjectDoesNotExist:
            once = RRule.objects.get(pk=1)
            today = date.today().weekday()
            default = Show.objects.get(pk=1)

            previous = TimeSlot.objects.filter(end__lte=datetime.now()).order_by('-start')[0]
            next = TimeSlot.objects.filter(start__gte=datetime.now())[0]

            dstart, tstart = previous.end.date(), previous.end.time()
            until, tend = next.start.date(), next.start.time()

            new_programslot = ProgramSlot(rrule=once, byweekday=today, show=default, dstart=dstart, tstart=tstart, tend=tend, until=until)
            new_programslot.save()

            return new_programslot.timeslots.all()[0]

class TimeSlot(models.Model):
    programslot = models.ForeignKey(ProgramSlot, related_name='timeslots', verbose_name=_("Program slot"))
    start = models.DateTimeField(_("Start time"), unique=True)
    end = models.DateTimeField(_("End time"))
    show = models.ForeignKey(Show, editable=False)

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

    @models.permalink
    def get_absolute_url(self):
        return ('timeslot-detail', [self.id])

class Note(models.Model):
    STATUS_CHOICES = (
        (0, _("Cancellation")),
        (1, _("Recommendation")),
        (2, _("Repetition")),
    )
    timeslot = models.OneToOneField(TimeSlot, verbose_name=_("Time slot"))
    owner = models.ForeignKey(User, related_name='notes', verbose_name=_("Owner"))
    title = models.CharField(_("Title"), max_length=128)
    content = models.TextField(_("Content"))
    status = models.IntegerField(_("Status"), choices=STATUS_CHOICES, default=1)
    cba_entry_id = models.IntegerField(_("CBA entry ID"), blank=True, null=True)
    start = models.DateTimeField(editable=False)
    show = models.ForeignKey(Show, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('timeslot',)
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")

    def __unicode__(self):
        return u'%s - %s' % (self.title, self.timeslot)

    def save(self, *args, **kwargs):
        self.start =  self.timeslot.start
        self.show = self.timeslot.programslot.show

        super(Note, self).save(*args, **kwargs)
