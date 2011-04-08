from haystack.indexes import CharField, DateTimeField, SearchIndex
from haystack import site

from datetime import datetime

from program.models import Note, Show

class NoteIndex(SearchIndex):
    SearchableText = CharField(document=True, use_template=True)

class ShowIndex(SearchIndex):
    SearchableText = CharField(document=True, use_template=True)

site.register(Note, NoteIndex)
site.register(Show, ShowIndex)
