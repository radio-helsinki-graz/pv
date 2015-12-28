from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Host, Note, ProgramSlot, Show, TimeSlot
from forms import MusicFocusForm

from datetime import date, datetime, timedelta


class BroadcastFormatAdmin(admin.ModelAdmin):
    list_display = ('format', 'enabled', 'admin_color')
    prepopulated_fields = {'slug': ('format',)}


class MusicFocusAdmin(admin.ModelAdmin):
    form = MusicFocusForm
    list_display = ('focus', 'abbrev', 'admin_buttons')
    prepopulated_fields = {'slug': ('focus',)}


class ShowInformationAdmin(admin.ModelAdmin):
    list_display = ('information', 'abbrev', 'admin_buttons')
    prepopulated_fields = {'slug': ('information',)}


class ShowTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'abbrev', 'admin_buttons')
    prepopulated_fields = {'slug': ('topic',)}


class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    list_display = ('title', 'show', 'start', 'status')
    list_filter = ('status',)
    ordering = ('timeslot',)
    save_as = True

    def queryset(self, request):
        shows = request.user.shows.all()
        return super(NoteAdmin, self).queryset(request).filter(show__in=shows)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        four_weeks = datetime.now() - timedelta(weeks=4)
        if db_field.name == 'timeslot':
            shows = request.user.shows.all()
            kwargs['queryset'] = TimeSlot.objects.filter(show__in=shows, start__gt=four_weeks)

        return super(NoteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.save()


class TimeSlotInline(admin.TabularInline):
    model = TimeSlot


class ProgramSlotAdmin(admin.ModelAdmin):
    actions = ('renew',)
    inlines = (TimeSlotInline,)
    list_display = ('show', 'byweekday', 'rrule', 'tstart', 'tend', 'until', 'timeslot_count')
    list_filter = ('byweekday', 'rrule', 'is_repetition')
    ordering = ('byweekday', 'dstart')
    save_on_top = True
    search_fields = ('show__name',)

    def renew(self, request, queryset):
        next_year = date.today().year + 1
        until = date(next_year, 12, 31)
        renewed = queryset.update(until=until)
        if renewed == 1:
            message = _("1 program slot was renewed until %s") % until
        else:
            message = _("%s program slots were renewed until %s") % until
        self.message_user(request, message)
    renew.short_description = _("Renew selected program slots")


class ProgramSlotInline(admin.TabularInline):
    model = ProgramSlot


class ShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('hosts', 'owners', 'musicfocus', 'showinformation', 'showtopic')
    inlines = (ProgramSlotInline,)
    list_display = ('name', 'short_description', 'broadcastformat', 'has_active_programslots')
    list_filter = ('broadcastformat', 'showinformation', 'showtopic', 'musicfocus')
    ordering = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')
    fields = (
        'predecessor', 'broadcastformat', 'name', 'slug', 'image', 'image_enabled', 'short_description', 'description',
        'email', 'website', 'cba_series_id', 'automation_id', 'hosts', 'owners', 'showinformation', 'showtopic',
        'musicfocus',
    )


admin.site.register(BroadcastFormat, BroadcastFormatAdmin)
admin.site.register(MusicFocus, MusicFocusAdmin)
admin.site.register(ShowInformation, ShowInformationAdmin)
admin.site.register(ShowTopic, ShowTopicAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(ProgramSlot, ProgramSlotAdmin)
admin.site.register(Show, ShowAdmin)

admin.site.register(Host)
