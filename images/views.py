from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from .forms import ImageCreateForm
from .models import Image
from actions.utils import create_action
import redis
from django.conf import settings
from django.utils.text import slugify

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
@require_GET
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 5)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
        if images_only:
            return HttpResponse('')
    if images_only:
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})
    else:
        return render(request, 'images/image/list.html', {'section': 'images', 'images': images})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'Liked', image)
            else:
                image.users_like.remove(request.user)
                create_action(request.user, 'Unliked', image)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
        return JsonResponse({"status": "error"})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)

    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image, 'total_views': total_views})


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST, request.FILES)
        print('POST')
        if form.is_valid():
            print('VALID')
            title = form.cleaned_data['title']
            user = request.user
            image = form.cleaned_data['image']
            print(f'image: {image}')
            description = form.cleaned_data['description']
            slug = slugify(title)
            newImage = Image.objects.create(
                title=title,
                user=user,
                image=image,
                slug=slug,
                description=description,
            )
            newImage.save()
            create_action(request.user, 'Added new picture', newImage)
            messages.success(request, 'Image added successfully')
            return redirect(newImage.get_absolute_url())
    else:
        form = ImageCreateForm(request.GET)
    return render(request, 'images/image/create.html',
                  {'section': 'images', 'form': form})


@login_required
def image_ranking(request):
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    index_map = {value: index for index, value in enumerate(image_ranking_ids)}
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed = sorted(most_viewed, key=lambda x: index_map[x.id])
    total_views_list = [int(r.get(f'image:{id}:views') or 0) for id in image_ranking_ids]
    most_viewed_data = dict(zip(most_viewed, total_views_list))
    most_liked = Image.objects.all().order_by('-total_likes')[:10]
    return render(request, 'images/image/ranking.html',
                  {'section': 'images', 'most_viewed': most_viewed_data, 'most_liked': most_liked})
