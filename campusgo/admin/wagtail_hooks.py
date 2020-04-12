from django.db import models
from django.utils.html import format_html
from django.templatetags.static import static
from wagtail.core import hooks
from wagtail.core.models import (
    Collection,
    GroupCollectionPermission,
)


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('campusgo_admin/css/admin_theme_2.css'))


def get_user_collections(request):
    """ Get user collections queryset """
    user = request.user
    collections = Collection.objects.all()
    if not user.is_superuser:
        groups = user.groups.all()
        if groups:
            collection_permissions = GroupCollectionPermission.objects.filter(group__in=groups)
            if collection_permissions:
                collection_pks = [cp.collection.pk for cp in collection_permissions.all()]
                collections = collections.filter(pk__in=collection_pks)
    return collections


@hooks.register('construct_document_chooser_queryset')
def document_chooser_based_on_collection_permissions(documents, request):
    """ Only show documents and collections owned by user """
    if request.user.is_superuser:
        return documents

    documents = documents.filter(
        models.Q(collection__in=get_user_collections(request))
        & models.Q(uploaded_by_user=request.user)
    )
    return documents


@hooks.register('construct_image_chooser_queryset')
def image_chooser_based_on_collection_permissions(images, request):
    """ Only show images and collections owned by user """
    if request.user.is_superuser:
        return images

    images = images.filter(
        models.Q(collection__in=get_user_collections(request))
        & models.Q(uploaded_by_user=request.user)
    )
    return images
