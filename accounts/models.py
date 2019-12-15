from django.db.models import CharField, Model, URLField


class Profile(Model):
    id = CharField(primary_key=True, max_length=33, editable=False)
    name = CharField(max_length=20)
    picture = URLField(max_length=128)

    class Meta:
        db_table = 'profile'
