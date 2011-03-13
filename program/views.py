from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic

from datetime import datetime, timedelta

class ShowListView(ListView):
    context_object_name = 'show_list'

    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)

        context['broadcastformat_list'] = BroadcastFormat.objects.all()
        context['musicfocus_list'] = MusicFocus.objects.all()
        context['showinformation_list'] = ShowInformation.objects.all()
        context['showtopic_list'] = ShowTopic.objects.all()

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
