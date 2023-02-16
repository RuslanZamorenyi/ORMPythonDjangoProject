from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q

from .models import GameModel, GamerLibraryModel, GamerModel

class FilterView(ListView):
    template_name = 'game_models.html'
    queryset = GameModel.objects.filter(
        ~Q(name__startswith="Ab") | ~Q(name__startswith="Ad") | ~Q(
            name__startswith="Mat"))


def relation_filter_view(request):
    data = GamerLibraryModel.objects.filter(gamer__email__contains="a")
    print(data[0].gamer.email)
    return HttpResponse(data.order_by())


class ExcludeView(ListView):
    template_name = 'game_models.html'
    queryset = GameModel.objects.exclude(name__contains="Hitman")


class OrderByView(ListView):
    template_name = 'game_models.html'
    # TODO add reverse
    queryset = GameModel.objects.exclude(name__contains="Hitman").order_by('year')


class AllView(ListView):
    template_name = 'game_models.html'
    queryset = GameModel.objects.all()


class UnionView(ListView):
    template_name = 'game_models.html'
    queryset = GameModel.objects.filter(name="Hitman (2016)").union(
        GameModel.objects.filter(name="Tetris"))


class NoneView(ListView):
    template_name = 'game_models.html'
    queryset = GameModel.objects.none()


class ValuesView(ListView):
    template_name = 'game_models.html'

    queryset = GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                     "platform",
                                                                     "year")

    def get(self, request, *args, **kwargs):
        print(GameModel.objects.filter(name="Hitman (2016)").values("name",
                                                                    "platform",
                                                                    "year"))
        print(list(
            GameModel.objects.all().values_list("name", 'year')))
        return super().get(request, *args, **kwargs)


def date_view(request):
    data = GameModel.objects.dates(field_name='year', kind='year')
    print(data)
    return HttpResponse(data)


def get_view(request):
    # TODO try error
    data = GameModel.objects.get(id=27)
    print(data)
    return HttpResponse(data)


def create_view(request):
    my_friend = GamerModel.objects.get(pk=10)
    my_friend.update(nickname="MySecondNickname")
    return HttpResponse(my_friend)


