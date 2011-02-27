from django.contrib import admin

from models import BroadcastFormat, MusicFocus, ShowInformation, ShowTopic, Host, Note, ProgramSlot, Show, TimeSlot

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
    list_filter = ('status',)
    ordering = ('time_slot',)

class TimeSlotInline(admin.TabularInline):
    model = TimeSlot

class ProgramSlotAdmin(admin.ModelAdmin):
    date_hierarchy = 'dstart'
    inlines = (TimeSlotInline,)
    list_display = ('show', 'byweekday', 'rrule', 'tstart', 'tend', 'dstart', 'until')
    list_filter = ('byweekday', 'rrule', 'is_repetition')
    ordering = ('byweekday', 'dstart')
    search_fields = ('show__name',)

class ProgramSlotInline(admin.TabularInline):
    model = ProgramSlot

class ShowAdmin(admin.ModelAdmin):
    filter_horizontal = ('hosts', 'owners', 'music_focus', 'show_information', 'show_topic')
    inlines = (ProgramSlotInline,)
    list_display = ('name', 'short_description', 'broadcast_format')
    list_filter = ('broadcast_format', 'show_information', 'show_topic', 'music_focus',)
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