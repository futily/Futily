import datetime
import json
import os
from urllib.parse import urlencode

import jinja2
import stringcase
from django.conf import settings
from django.urls import reverse
from django.utils import six, timezone
from django.utils.safestring import mark_safe
from django_jinja import library
from sorl.thumbnail import get_thumbnail

# from ..models import Footer, Header


def _navigation_entries(context, pages, section=None, is_json=False):
    request = context["request"]
    # Compile the entries.

    def page_entry(page):
        # Do nothing if the page is to be hidden from not logged in users
        if page.hide_from_anonymous and not request.user.is_authenticated():
            return

        url = page.get_absolute_url()

        children = []

        navigation_items = getattr(page.content, 'navigation_items', None)
        if navigation_items:
            children = [{
                'url': url,
                'title': label,
                'here': request.path.startswith(url),
                'separator': label == '-',
                'children': []
            } for (label, url) in navigation_items]

        if is_json:
            return {
                "url": url,
                "title": six.text_type(page),
                "here": request.path.startswith(url),
                "children": children + [page_entry(x) for x in page.navigation if
                                        page is not request.pages.homepage]
            }
        return {
            "url": url,
            "page": page,
            "title": six.text_type(page),
            "here": request.path.startswith(url),
            "children": children + [page_entry(x) for x in page.navigation if page is not request.pages.homepage]
        }

    # All the applicable nav items
    entries = [page_entry(x) for x in pages if page_entry(x) is not None]

    # Add the section.
    if section:
        section_entry = page_entry(section)
        section_entry["here"] = context["pages"].current == section_entry["page"]
        entries = [section_entry] + list(entries)

    return entries


@library.global_function
@library.render_with('pages/navigation.html')
@jinja2.contextfunction
def render_navigation(context, pages, section=None):
    """
    Renders a navigation list for the given pages.

    The pages should all be a subclass of PageBase, and possess a get_absolute_url() method.

    You can also specify an alias for the navigation, at which point it will be set in the
    context rather than rendered.
    """
    return {
        "navigation": _navigation_entries(context, pages, section),
    }


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


@library.global_function
@jinja2.contextfunction
def path_to_url(context, path):
    if path.startswith('http://') or path.startswith('https://'):
        return path

    if not path.startswith('/'):
        path = '/' + path

    if context['request'].is_secure():
        secure_part = 's'
    else:
        secure_part = ''

    return 'http{}://{}{}'.format(secure_part, settings.SITE_DOMAIN, path)


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
    return_url = kwargs.pop('initial_url', f'{request.path}')

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


@library.filter
def camel_case(value):
    camel_case_string = stringcase.camelcase(value).replace('_', '')

    return camel_case_string


@library.filter
def is_older_than(time, hours):
    return time + datetime.timedelta(hours=hours) > timezone.now()
