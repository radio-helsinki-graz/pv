from django.views.generic.list import ListView

from models import BroadcastFormat, MusicFocus, Show, ShowInformation, ShowTopic

class ShowListView(ListView):
    context_object_name = 'show_list'
    model = Show

    def get_context_data(self, **kwargs):
        context = super(ShowListView, self).get_context_data(**kwargs)

        context['broadcast_format_list'] = BroadcastFormat.objects.all()
        context['music_focus_list'] = MusicFocus.objects.all()
        context['show_information_list'] = ShowInformation.objects.all()
        context['show_topic_list'] = ShowTopic.objects.all()

        return context