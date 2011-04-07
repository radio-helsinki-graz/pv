from haystack.indexes import CharField, DateTimeField, SearchIndex
from haystack import site

from datetime import datetime

from program.models import Note, Show

class NoteIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    last_updated = DateTimeField(model_attr='last_updated')

    def get_queryset(self):
        return Note.objects.filter(last_updated__lte=datetime.now())

class ShowIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    last_updated = DateTimeField(model_attr='last_updated')

    def get_queryset(self):
        return Show.objects.filter(last_updated__lte=datetime.now())

site.register(Note, NoteIndex)
site.register(Show, ShowIndex)