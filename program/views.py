from django.views.generic import ListView

from models import BroadcastFormat, MusicFocus, Note, Show, ShowInformation, ShowTopic

from datetime import datetime, timedelta

class ShowListView(ListView):
    context_object_name = 'show_list'
    model = Show

    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)

        context['broadcastformat_list'] = BroadcastFormat.objects.all()
        context['musicfocus_list'] = MusicFocus.objects.all()
        context['showinformation_list'] = ShowInformation.objects.all()
        context['showtopic_list'] = ShowTopic.objects.all()

        return context

class RecommendationsView(ListView):
    now = datetime.now()
    in_one_week = now + timedelta(weeks=1)
    context_object_name = 'recommendation_list'
    template_name = 'program/recommendations.html'
    queryset = Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:10]

class RecommendationsBoxView(RecommendationsView):
    now = datetime.now()
    in_one_week = now + timedelta(weeks=1)
    queryset = Note.objects.filter(status=1, timeslot__start__range=(now, in_one_week))[:3]
