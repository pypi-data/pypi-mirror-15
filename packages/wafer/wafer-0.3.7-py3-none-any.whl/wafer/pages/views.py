from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, TemplateView, UpdateView

from reversion import revisions
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from wafer.pages.models import Page
from wafer.pages.serializers import PageSerializer
from wafer.pages.forms import PageForm


class ShowPage(DetailView):
    template_name = 'wafer.pages/page.html'
    model = Page


class EditPage(UpdateView):
    template_name = 'wafer.pages/page_form.html'
    model = Page
    form_class = PageForm

    @revisions.create_revision()
    def form_valid(self, form):
        revisions.set_user(self.request.user)
        revisions.set_comment("Page Modified")
        return super(EditPage, self).form_valid(form)


def slug(request, url):
    """Look up a page by url (which is a tree of slugs)"""
    page = None

    if url:
        for slug in url.split('/'):
            if not slug:
                continue
            try:
                page = Page.objects.get(slug=slug, parent=page)
            except Page.DoesNotExist:
                raise Http404
    else:
        try:
            page = Page.objects.get(slug='index')
        except Page.DoesNotExist:
            return TemplateView.as_view(
                template_name='wafer/index.html')(request)

    if 'edit' in request.GET:
        if not request.user.has_perm('pages.change_page'):
            raise PermissionDenied
        return EditPage.as_view()(request, pk=page.id)

    return ShowPage.as_view()(request, pk=page.id)


class PageViewSet(viewsets.ModelViewSet):
    """API endpoint for users."""
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )
