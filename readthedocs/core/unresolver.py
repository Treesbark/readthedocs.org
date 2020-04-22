from urllib.parse import urlparse

from django.urls import resolve as url_resolve
from django.test.client import RequestFactory

from readthedocs.proxito.middleware import map_host_to_project_slug
from readthedocs.proxito.views.utils import _get_project_data_from_request


def unresolve(uri):
    """
    Turn a URL into the component parts that our views would use to process them.

    This is useful for lots of places,
    like where we want to figure out exactly what file a URL maps to
    """
    parsed = urlparse(uri)
    rf = RequestFactory()
    domain = parsed.netloc.split(':', 1)[0]
    path = parsed.path

    request = rf.get(path=path, HTTP_HOST=domain)
    project_slug = map_host_to_project_slug(request)

    _, __, kwargs = url_resolve(
        path,
        urlconf='readthedocs.proxito.urls',
    )

    # TODO: support external builds
    # mixin = ServeDocsMixin()
    # version_slug = mixin.get_version_from_host(request, version_slug)

    final_project, lang_slug, version_slug, filename = _get_project_data_from_request(  # noqa
        request,
        project_slug=project_slug,
        subproject_slug=kwargs.get('subproject_slug'),
        lang_slug=kwargs.get('lang_slug'),
        version_slug=kwargs.get('version_slug'),
        filename=kwargs.get('filename', ''),
    )
    return (final_project, lang_slug, version_slug, filename)
