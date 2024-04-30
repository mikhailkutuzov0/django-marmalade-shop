from django.contrib.postgres.search import (
    SearchQuery, SearchVector, SearchRank, SearchHeadline
)
from goods.models import Products


def q_search(query):
    """
    Выполняет поиск , используя возможности полнотекстового поиска Django.

    Может искать по id товара, если запрос состоит только из цифр и не
    превышает 5 символов, или по полям 'name' и 'description', используя
    введенный поисковый запрос.

    Args:
        query (str): Строка запроса, введенная пользователем.

    Returns:
        QuerySet: Набор найденных объектов, отсортированных по релевантности,
        найденных фрагментов в названии и описании.
    """
    # Проверка, является ли запрос числовым и длина меньше 6 (поиск по ID)
    if query.isdigit() and len(query) <= 5:
        # Возврат продуктов по ID
        return Products.objects.filter(id=int(query))

    # Создание вектора поиска и поискового запроса для полнотекстового поиска
    vector = SearchVector("name", "description")
    query = SearchQuery(query)

    # Аннотация набора данных с рангом релевантности поиска и фильтрация
    result = (
        Products.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    # Добавление аннотаций для выделения найденных фрагментов
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )

    return result
