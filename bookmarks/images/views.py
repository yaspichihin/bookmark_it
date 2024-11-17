import redis
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from django.conf import settings
from actions.utils import create_action
from .forms import ImageCreateForm
from .models import Image

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


@login_required
def image_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, "bookmarked image", new_image)
            messages.success(
                request=request,
                message="Image added successfully",
            )
            # Перенаправить к представлению детальной информации
            # о только что созданном элементе.
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request=request,
        template_name="images/image/create.html",
        context={"form": form},
    )


def image_detail(
    request: HttpRequest,
    id_: int,
    slug: str,
) -> HttpResponse:
    image = get_object_or_404(Image, id=id_, slug=slug)

    # Увеличить кол-во просмотров на 1
    total_views = r.incr(f"image:{image.id}:views")

    # Увеличить рейтинг изображения на 1
    r.zincrby("image_ranking", 1, image.id)

    return render(
        request,
        template_name="images/image/detail.html",
        context={
            "section": "images",
            "image": image,
            "total_views": total_views,
        },
    )


@login_required
@require_POST
def image_like(request: HttpRequest) -> HttpResponse:
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.users_like.add(request.user)
                create_action(request.user, "likes", image)

            else:
                image.users_like.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": "error"})


@login_required
def image_list(request: HttpRequest) -> HttpResponse:
    images = Image.objects.all()
    paginator = Paginator(images, per_page=8)
    page = request.GET.get("page")
    images_only = request.GET.get("images_only")

    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, то 1 страница
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # Если AJAX-запрос и страница вне диапазона,
            # то вернуть пустую страницу.
            return HttpResponse("")
        # Если страница вне диапазона вернуть последнюю страницу
        images = paginator.page(paginator.num_pages)

    if images_only:
        return render(
            request,
            template_name="images/image/list_images.html",
            context={"section": "images", "images": images},
        )

    return render(
        request,
        template_name="images/image/list.html",
        context={"section": "images", "images": images},
    )


@login_required
def image_ranking(request: HttpRequest) -> HttpResponse:

    # Получить словарь рейтинга изображений
    image_ranking = r.zrange(
        name="image_ranking",
        start=0,
        end=-1,
        desc=True,
    )[:10]

    image_ranking_ids = [int(id_) for id_ in image_ranking]

    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))

    # Сортировать по индексу появления в рейтинге изображений
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

    return render(
        request=request,
        template_name="images/image/ranking.html",
        context={"section": "images", "most_viewed": most_viewed},
    )
