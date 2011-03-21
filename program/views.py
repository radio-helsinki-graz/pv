from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.shortcuts import get_object_or_404

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic, TimeSlot

from datetime import date, datetime, time, timedelta

class ShowListView(ListView):
    context_object_name = 'shows'

    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)

        context['broadcastformats'] = BroadcastFormat.objects.all()
        context['musicfoci'] = MusicFocus.objects.all()
        context['showinformations'] = ShowInformation.objects.all()
        context['showtopics'] = ShowTopic.objects.all()

        return context

    def get_queryset(self):
        if 'broadcastformat' in self.request.GET:
            broadcastformat = get_object_or_404(BroadcastFormat, slug=self.request.GET['broadcastformat'])

            return Show.objects.filter(broadcastformat=broadcastformat)
        elif 'musicfocus' in self.request.GET:
            musicfocus = get_object_or_404(MusicFocus, slug=self.request.GET['musicfocus'])

            return Show.objects.filter(musicfocus=musicfocus)
        elif 'showinformation' in self.request.GET:
            showinformation = get_object_or_404(ShowInformation, slug=self.request.GET['showinformation'])

            return Show.objects.filter(showinformation=showinformation)
        elif 'showtopic' in self.request.GET:
            showtopic = get_object_or_404(ShowTopic, slug=self.request.GET['showtopic'])

            return Show.objects.filter(showtopic=showtopic)
        else:
            return Show.objects.all()

class RecommendationsView(ListView):
    context_object_name = 'recommendations'
    template_name = 'program/recommendations.html'

    def get_queryset(self):
        now = datetime.now()
        in_one_week = now + timedelta(weeks=1)

        return Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:10]

class TodayScheduleView(TodayArchiveView):
    model = TimeSlot
    allow_future = True
    date_field = 'start'
    context_object_name = 'timeslots'
    template_name = 'program/today_schedule.html'

    def get_context_data(self, **kwargs):
        context = super(TodayScheduleView, self).get_context_data(**kwargs)

        now = datetime.now()
        midnight = datetime.combine(date.today(), time(23, 59))

        context['broadcastformats'] = BroadcastFormat.objects.all()
        context['recommendations'] = Note.objects.filter(status=1, timeslot__start__range=(now, midnight))

        return context

class DayScheduleView(DayArchiveView):
    model = TimeSlot
    allow_future = True
    date_field = 'start'
    month_format = '%m'
    context_object_name = 'timeslots'
    template_name = 'program/day_schedule.html'

    def get_context_data(self, **kwargs):
        context = super(DayScheduleView, self).get_context_data(**kwargs)

        year, month, day = map(int, [self.get_year(), self.get_month(), self.get_day()])
        this_day = datetime(year, month, day, 0, 0)
        midnight = datetime(year, month, day, 23, 59)
        
        context['broadcastformats'] = BroadcastFormat.objects.all()
        context['recommendations'] = Note.objects.filter(status=1, timeslot__start__range=(this_day, midnight))

        return context
    
class CurrentShowView(TemplateView):
    template_name = 'program/current.html'

    def get_context_data(self, **kwargs):
        context = super(CurrentShowView, self).get_context_data(**kwargs)

        context['current'] = TimeSlot.objects.get_or_create_current()
        context['next'] = TimeSlot.objects.get_or_create_current().get_next_by_start()
        context['after_next'] = TimeSlot.objects.get_or_create_current().get_next_by_start().get_next_by_start()

        return context