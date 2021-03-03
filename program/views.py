import json
from datetime import date, datetime, time, timedelta

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic, Language, TimeSlot, Host

from program.utils import tofirstdayinisoweek, get_cached_shows


# Legacy Views for Homepage until 2021

class HostListView(ListView):
    context_object_name = 'host_list'
    queryset = Host.objects.filter(Q(is_always_visible=True) | Q(shows__programslots__until__gt=datetime.now)).distinct()
    template_name = 'host_list.html'


class HostDetailView(DetailView):
    context_object_name = 'host'
    queryset = Host.objects.all()
    template_name = 'host_detail.html'


class ShowListView(ListView):
    context_object_name = 'show_list'
    template_name = 'show_list.html'

    def get_queryset(self):
        queryset = Show.objects.filter(programslots__until__gt=date.today()).exclude(id=1).distinct()
        if 'broadcastformat' in self.request.GET:
            broadcastformat = get_object_or_404(BroadcastFormat, slug=self.request.GET['broadcastformat'])
            queryset = queryset.filter(broadcastformat=broadcastformat)
        elif 'musicfocus' in self.request.GET:
            musicfocus = get_object_or_404(MusicFocus, slug=self.request.GET['musicfocus'])
            queryset = queryset.filter(musicfocus=musicfocus)
        elif 'showinformation' in self.request.GET:
            showinformation = get_object_or_404(ShowInformation, slug=self.request.GET['showinformation'])
            queryset = queryset.filter(showinformation=showinformation)
        elif 'showtopic' in self.request.GET:
            showtopic = get_object_or_404(ShowTopic, slug=self.request.GET['showtopic'])
            queryset = queryset.filter(showtopic=showtopic)
        elif 'language' in self.request.GET:
            language = get_object_or_404(Language, slug=self.request.GET['language'])
            queryset = queryset.filter(language=language)

        return queryset


class ShowDetailView(DetailView):
    queryset = Show.objects.all().exclude(id=1)
    template_name = 'show_detail.html'


class TimeSlotDetailView(DetailView):
    queryset = TimeSlot.objects.all()
    template_name = 'timeslot_detail.html'


class RecommendationsListView(ListView):
    context_object_name = 'recommendation_list'
    template_name = 'recommendation_list.html'

    now = datetime.now()
    end = now + timedelta(weeks=1)

    queryset = TimeSlot.objects.filter(Q(note__isnull=False, note__status=1,
                                         start__range=(now, end)) |
                                       Q(show__broadcastformat__slug='sondersendung',
                                         start__range=(now, end))).order_by('start')[:20]


class RecommendationsBoxView(RecommendationsListView):
    template_name = 'boxes/recommendation.html'


class DayScheduleView(TemplateView):
    template_name = 'day_schedule.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)

        if year is None and month is None and day is None:
            today = datetime.combine(date.today(), time(6, 0))
        else:
            today = datetime.strptime('%s__%s__%s__06__00' % (year, month, day), '%Y__%m__%d__%H__%M')

        tomorrow = today + timedelta(days=1)

        context = super(DayScheduleView, self).get_context_data(**kwargs)
        context['day'] = today
        context['recommendations'] = Note.objects.filter(status=1, timeslot__start__range=(today, tomorrow))
        context['default_show'] = Show.objects.get(pk=1)

        timeslots = TimeSlot.objects.get_day_timeslots(today)

        if 'broadcastformat' in self.request.GET:
            broadcastformat = get_object_or_404(BroadcastFormat, slug=self.request.GET['broadcastformat'])
            context['timeslots'] = timeslots.filter(show__broadcastformat=broadcastformat)
        elif 'musicfocus' in self.request.GET:
            musicfocus = get_object_or_404(MusicFocus, slug=self.request.GET['musicfocus'])
            context['timeslots'] = timeslots.filter(show__musicfocus=musicfocus)
        elif 'showinformation' in self.request.GET:
            showinformation = get_object_or_404(ShowInformation, slug=self.request.GET['showinformation'])
            context['timeslots'] = timeslots.filter(show__showinformation=showinformation)
        elif 'showtopic' in self.request.GET:
            showtopic = get_object_or_404(ShowTopic, slug=self.request.GET['showtopic'])
            context['showtopic'] = timeslots.filter(show__showtopic=showtopic)
        elif 'language' in self.request.GET:
            language = get_object_or_404(Language, slug=self.request.GET['language'])
            context['showtopic'] = timeslots.filter(show__language=language)
        else:
            context['timeslots'] = timeslots
        return context


class CurrentShowBoxView(TemplateView):
    context_object_name = 'recommendation_list'
    template_name = 'boxes/current.html'

    def get_context_data(self, **kwargs):
        current_timeslot = TimeSlot.objects.get_or_create_current()
        previous_timeslot = current_timeslot.get_previous_by_start()
        next_timeslot = current_timeslot.get_next_by_start()
        after_next_timeslot = next_timeslot.get_next_by_start()

        context = super(CurrentShowBoxView, self).get_context_data(**kwargs)
        context['current_timeslot'] = current_timeslot
        context['previous_timeslot'] = previous_timeslot
        context['next_timeslot'] = next_timeslot
        context['after_next_timeslot'] = after_next_timeslot
        return context


class WeekScheduleView(TemplateView):
    template_name = 'week_schedule.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year', None)
        week = self.kwargs.get('week', None)

        if year is None and week is None:
            year, week = datetime.now().strftime('%G__%V').split('__')

        monday = tofirstdayinisoweek(int(year), int(week))
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = monday + timedelta(days=6)

        context = super(WeekScheduleView, self).get_context_data()
        context['monday'] = monday
        context['tuesday'] = tuesday
        context['wednesday'] = wednesday
        context['thursday'] = thursday
        context['friday'] = friday
        context['saturday'] = saturday
        context['sunday'] = sunday
        context['default_show'] = Show.objects.get(pk=1)
        context['monday_timeslots'] = TimeSlot.objects.get_day_timeslots(monday)
        context['tuesday_timeslots'] = TimeSlot.objects.get_day_timeslots(tuesday)
        context['wednesday_timeslots'] = TimeSlot.objects.get_day_timeslots(wednesday)
        context['thursday_timeslots'] = TimeSlot.objects.get_day_timeslots(thursday)
        context['friday_timeslots'] = TimeSlot.objects.get_day_timeslots(friday)
        context['saturday_timeslots'] = TimeSlot.objects.get_day_timeslots(saturday)
        context['sunday_timeslots'] = TimeSlot.objects.get_day_timeslots(sunday)
        context['last_w'] = datetime.strftime(monday - timedelta(days=7), '%G/%V')
        context['current_year'] = datetime.strftime(monday, '%G')
        context['current_week'] = datetime.strftime(monday, '%V')
        context['cur_w'] = datetime.strftime(monday, '%G/%V')
        context['next_w1'] = datetime.strftime(monday + timedelta(days=7), '%G/%V')
        context['next_w2'] = datetime.strftime(monday + timedelta(days=14), '%G/%V')
        context['next_w3'] = datetime.strftime(monday + timedelta(days=21), '%G/%V')
        context['next_w4'] = datetime.strftime(monday + timedelta(days=28), '%G/%V')
        return context


class StylesView(TemplateView):
    template_name = 'styles.css'
    content_type = 'text/css'

    def get_context_data(self, **kwargs):
        context = super(StylesView, self).get_context_data(**kwargs)
        context['broadcastformats'] = BroadcastFormat.objects.filter(enabled=True)
        context['musicfocus'] = MusicFocus.objects.all()
        context['showinformation'] = ShowInformation.objects.all()
        context['showtopic'] = ShowTopic.objects.all()
        return context


# V2 Views added for new Homepage 2021

class HostListViewV2(ListView):
    context_object_name = 'host_list'
    queryset = Host.objects.filter(Q(is_always_visible=True) | Q(shows__programslots__until__gt=datetime.now)).distinct()
    template_name = 'v2/host_list.html'


class HostDetailViewV2(DetailView):
    context_object_name = 'host'
    queryset = Host.objects.all()
    template_name = 'v2/host_detail.html'


class ShowListViewV2(ListView):
    context_object_name = 'show_list'
    template_name = 'v2/show_list.html'

    def get_queryset(self):
        queryset = Show.objects.filter(programslots__until__gt=date.today()).exclude(id=1).distinct()
        if 'broadcastformat' in self.request.GET:
            broadcastformat = get_object_or_404(BroadcastFormat, slug=self.request.GET['broadcastformat'])
            queryset = queryset.filter(broadcastformat=broadcastformat)
        elif 'musicfocus' in self.request.GET:
            musicfocus = get_object_or_404(MusicFocus, slug=self.request.GET['musicfocus'])
            queryset = queryset.filter(musicfocus=musicfocus)
        elif 'showinformation' in self.request.GET:
            showinformation = get_object_or_404(ShowInformation, slug=self.request.GET['showinformation'])
            queryset = queryset.filter(showinformation=showinformation)
        elif 'showtopic' in self.request.GET:
            showtopic = get_object_or_404(ShowTopic, slug=self.request.GET['showtopic'])
            queryset = queryset.filter(showtopic=showtopic)
        elif 'language' in self.request.GET:
            language = get_object_or_404(Language, slug=self.request.GET['language'])
            queryset = queryset.filter(language=language)

        return queryset


class ShowDetailViewV2(DetailView):
    queryset = Show.objects.all().exclude(id=1)
    template_name = 'v2/show_detail.html'


class TimeSlotDetailViewV2(DetailView):
    queryset = TimeSlot.objects.all()
    template_name = 'v2/timeslot_detail.html'


class RecommendationsListViewV2(ListView):
    context_object_name = 'recommendation_list'
    template_name = 'v2/recommendation_list.html'

    now = datetime.now()
    end = now + timedelta(weeks=1)

    queryset = TimeSlot.objects.filter(Q(note__isnull=False, note__status=1,
                                         start__range=(now, end)) |
                                       Q(show__broadcastformat__slug='sondersendung',
                                         start__range=(now, end))).order_by('start')[:20]


class DayScheduleViewV2(TemplateView):
    template_name = 'v2/day_schedule.html'

    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)
        day = self.kwargs.get('day', None)

        if year is None and month is None and day is None:
            today = datetime.combine(date.today(), time(6, 0))
        else:
            today = datetime.strptime('%s__%s__%s__06__00' % (year, month, day), '%Y__%m__%d__%H__%M')

        tomorrow = today + timedelta(days=1)

        context = super(DayScheduleViewV2, self).get_context_data(**kwargs)
        context['day'] = today
        context['recommendations'] = Note.objects.filter(status=1, timeslot__start__range=(today, tomorrow))
        context['default_show'] = Show.objects.get(pk=1)

        timeslots = TimeSlot.objects.get_day_timeslots(today)

        if 'broadcastformat' in self.request.GET:
            broadcastformat = get_object_or_404(BroadcastFormat, slug=self.request.GET['broadcastformat'])
            context['timeslots'] = timeslots.filter(show__broadcastformat=broadcastformat)
        elif 'musicfocus' in self.request.GET:
            musicfocus = get_object_or_404(MusicFocus, slug=self.request.GET['musicfocus'])
            context['timeslots'] = timeslots.filter(show__musicfocus=musicfocus)
        elif 'showinformation' in self.request.GET:
            showinformation = get_object_or_404(ShowInformation, slug=self.request.GET['showinformation'])
            context['timeslots'] = timeslots.filter(show__showinformation=showinformation)
        elif 'showtopic' in self.request.GET:
            showtopic = get_object_or_404(ShowTopic, slug=self.request.GET['showtopic'])
            context['showtopic'] = timeslots.filter(show__showtopic=showtopic)
        elif 'language' in self.request.GET:
            language = get_object_or_404(Language, slug=self.request.GET['language'])
            context['showtopic'] = timeslots.filter(show__language=language)
        else:
            context['timeslots'] = timeslots
        return context


# Exports

def json_day_schedule(request, year=None, month=None, day=None):
    if year is None and month is None and day is None:
        today = datetime.combine(date.today(), time(0, 0))
    else:
        today = datetime.strptime('%s__%s__%s__00__00' % (year, month, day), '%Y__%m__%d__%H__%M')

    timeslots = TimeSlot.objects.get_24h_timeslots(today).select_related('programslot').select_related('show')
    schedule = []
    for ts in timeslots:
        entry = {
            'start': ts.start.strftime('%Y-%m-%d_%H:%M:%S'),
            'end': ts.end.strftime('%Y-%m-%d_%H:%M:%S'),
            'title': ts.show.name,
            'id': ts.show.id,
            'automation-id': -1
        }

        if ts.programslot.automation_id:
            entry['automation-id'] = ts.programslot.automation_id

        schedule.append(entry)

    return HttpResponse(json.dumps(schedule, ensure_ascii=False, encoding='utf8').encode('utf8'),
                        content_type="application/json; charset=utf-8")


def json_timeslots_specials(request):
    specials = {}
    shows = get_cached_shows()['shows']
    for show in shows:
        show['pv_id'] = -1
        if show['type'] == 's':
            specials[show['id']] = show

    for ts in TimeSlot.objects.filter(end__gt=datetime.now, programslot__automation_id__in=specials.iterkeys()).select_related('show'):
        automation_id = ts.programslot.automation_id
        start = ts.start.strftime('%Y-%m-%d_%H:%M:%S')
        end = ts.end.strftime('%Y-%m-%d_%H:%M:%S')
        if specials[automation_id]['pv_id'] != -1:
            if specials[automation_id]['pv_start'] < start:
                continue

        specials[automation_id]['pv_id'] = int(ts.show.id)
        specials[automation_id]['pv_name'] = ts.show.name
        specials[automation_id]['pv_start'] = start
        specials[automation_id]['pv_end'] = end

    return HttpResponse(json.dumps(specials, ensure_ascii=False, encoding='utf8').encode('utf8'),
                        content_type="application/json; charset=utf-8")
