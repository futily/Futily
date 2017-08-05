import json
import os
from urllib.parse import urlencode

import jinja2
from cms.apps.pages.templatetags.pages import _navigation_entries
from django.conf import settings
from django.urls import reverse
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail

# from ..models import Footer, Header


@library.global_function
@jinja2.contextfunction
def get_navigation_json(context, pages, section=None):
    return json.dumps(_navigation_entries(context, pages, section, is_json=True))


@library.global_function
def frontend_templates():
    return mark_safe([
        str(f[:-5])
        for f in os.listdir(os.path.join(settings.TEMPLATES[0]['DIRS'][0], 'frontend'))
        if f[:1] != '_'
    ])


# Usage: get_next_by_field(obj, 'date')
@library.global_function
def get_next_by_field(obj, field):
    try:
        return getattr(obj, 'get_next_by_{}'.format(field))()
    except obj.DoesNotExist:
        return obj._default_manager.last()
    except Exception:  # pylint:disable=broad-except
        pass  # Will cause 'None' to be returned.


# Usage: get_previous_by_field(obj, 'date')
@library.global_function
def get_previous_by_field(obj, field):
    try:
        return getattr(obj, 'get_previous_by_{}'.format(field))()
    except obj.DoesNotExist:
        return obj._default_manager.first()
    except Exception:  # pylint:disable=broad-except
        pass  # Will cause 'None' to be returned.


@library.global_function
@library.render_with('images/lazy.html')
@library.global_function
@library.render_with('images/lazy.html')
def lazy_image(image, height=None, width=None, blur=True, max_width=1920):
    """
    Usage: {{ lazy_image(path.to.image) }}

    :param max_width:
    :param blur:
    :param image:
    :param height:
    :param width
    :return:
    """

    # Ideally we will use the images uploaded sizes to get our aspect ratio but in certain circumstances, like cards,
    # we will use our own provided ones
    if not height:
        height = image.height

    if not width:
        width = image.width

    aspect_ratio = height / width

    if width > max_width:
        width = max_width

    # The aspect ratio will be used to size the image with a padding-bottom based element
    aspect_ratio_percentage = '{}%'.format(aspect_ratio * 100)
    small_image_url = get_thumbnail(image.file, str(int(width / 20))).url
    large_image_url = get_thumbnail(image.file, str(width)).url

    return {
        'image_obj': image,
        'aspect_ratio': aspect_ratio_percentage,
        'small_image_url': small_image_url,
        'large_image_url': large_image_url,
        'blur': blur
    }


# @library.global_function
# def get_header_content():
#     try:
#         return Header.objects.first()
#     except IndexError:
#         return None
#
#
# @library.global_function
# def get_footer_content():
#     try:
#         return Footer.objects.first()
#     except IndexError:
#         return None


@jinja2.contextfunction
@library.global_function
def build_url(context, *args, **kwargs):
    request = context['request']
    get = kwargs.pop('get', {})
    remove = kwargs.pop('remove', '')
    return_url = f'{request.path}'

    # Sometimes no 'viewname' is passed i.e. building pagination links
    if args or kwargs:
        return_url = reverse(*args, **kwargs)

    if hasattr(request.GET, 'dict'):
        params = request.GET.dict()

        # If we want to change something more than likely we want to
        # reset the current page, so remove the page param
        if 'page' in params and get:
            params.pop('page')

        if remove:
            for item in remove:
                params.pop(item, None)

        params.update(**get)

        return_url += '?{}'.format(urlencode(params))

    if return_url == f'{request.path}?':
        return request.path

    return return_url


@library.global_function
@library.render_with('pagination/pagination.html')
@jinja2.contextfunction
def render_pagination(context, page_obj, offset=2, pagination_key=None):
    """Renders the pagination for the given page of items."""
    current_page = page_obj.number
    offset_indexes = [x for x in range(current_page - offset, current_page + (offset + 1)) if x >= 1]

    return {
        "request": context["request"],
        "offset_indexes": offset_indexes,
        "offset": offset,
        "page_obj": page_obj,
        "paginator": page_obj.paginator,
        "pagination_key": pagination_key or getattr(page_obj, "_pagination_key", "page")
    }
