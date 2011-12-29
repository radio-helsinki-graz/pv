from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Host, Note, ProgramSlot, Show, TimeSlot

from datetime import date

class BroadcastFormatAdmin(admin.ModelAdmin):
    list_display = ('format',)
    prepopulated_fields = {'slug': ('format',)}

class MusicFocusAdmin(admin.ModelAdmin):
    list_display = ('focus', 'abbrev')
    prepopulated_fields = {'slug': ('focus',)}

class ShowInformationAdmin(admin.ModelAdmin):
    list_display = ('information', 'abbrev')
    prepopulated_fields = {'slug': ('information',)}

class ShowTopicAdmin(admin.ModelAdmin):
    list_display = ('topic', 'abbrev')
    prepopulated_fields = {'slug': ('topic',)}

class NoteAdmin(admin.ModelAdmin):
    date_hierarchy = 'start'
    exclude = ('owner',)
    list_display = ('title', 'show', 'start', 'status')
    list_filter = ('status',)
    ordering = ('timeslot',)

    def queryset(self, request):
        shows = request.user.shows.all()
        return super(NoteAdmin, self).queryset(request).filter(show__in=shows)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'timeslot':
            shows = request.user.shows.all()
            kwargs['queryset'] = TimeSlot.objects.filter(show__in=shows)

        return super(NoteAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

class TimeSlotInline(admin.TabularInline):
    max_num = 2
    model = TimeSlot

def renew(modeladmin, request, queryset):
    next_year = date.today().year+1
    queryset.update(until=date(next_year, 12, 31))
renew.short_description = _("Renew selected time slots")

class ProgramSlotAdmin(admin.ModelAdmin):
    actions = (renew,)
    inlines = (TimeSlotInline,)
    list_display = ('show', 'byweekday', 'rrule', 'tstart', 'tend', 'until', 'timeslot_count')
    list_filter = ('byweekday', 'rrule', 'is_repetition')
    ordering = ('byweekday', 'dstart')
    save_on_top = True
    search_fields = ('show__name',)

class ProgramSlotInline(admin.TabularInline):
    max_num = 2
    model = ProgramSlot

class ShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('hosts', 'owners', 'musicfocus', 'showinformation', 'showtopic')
    inlines = (ProgramSlotInline,)
    list_display = ('name', 'short_description', 'broadcastformat', 'has_active_programslots')
    list_filter = ('broadcastformat', 'showinformation', 'showtopic', 'musicfocus',)
    ordering = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_description', 'description')

admin.site.register(BroadcastFormat, BroadcastFormatAdmin)
admin.site.register(MusicFocus, MusicFocusAdmin)
admin.site.register(ShowInformation, ShowInformationAdmin)
admin.site.register(ShowTopic, ShowTopicAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(ProgramSlot, ProgramSlotAdmin)
admin.site.register(Show, ShowAdmin)

admin.site.register(Host)