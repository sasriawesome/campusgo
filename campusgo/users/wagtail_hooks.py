from django.contrib.auth.models import Group, Permission
from wagtail.core import hooks
from wagtail.core.models import (
    Collection,
    GroupCollectionPermission,
    CollectionViewRestriction
)


@hooks.register('after_create_user')
def create_group_and_collection_for_user(request, user):
    """ Create private collection and group for given User """

    group_prefix = 'USER_GROUP_'
    collection_prefix = 'USER_COLLECTION_'

    # create user's private_group and bind to user
    group_name = '%s_%s_%s' % (group_prefix, user.username, str(user.id).replace('-', '')[0:8])
    group, new_group = Group.objects.get_or_create(
        name=group_name,
        defaults={'name': group_name}
    )

    # create user's private_collection
    collection_name = '%s_%s_%s' % (collection_prefix, user.username, str(user.id).replace('-', '')[0:8])
    collection = Collection(name=collection_name)
    root_collection = Collection.get_first_root_node()
    root_collection.add_child(instance=collection)

    # add group collection permissions
    permissions = Permission.objects.filter(
        codename__in=['add_image', 'add_document']
    )
    group_object_permissions = []
    for perm in permissions:
        group_object_permissions.append(
            GroupCollectionPermission(
                group=group,
                collection=collection,
                permission=perm
            )
        )
    GroupCollectionPermission.objects.bulk_create(
        group_object_permissions
    )

    # Setup CollectionViewRestriction to private for user's group
    restriction = CollectionViewRestriction.objects.create(
        restriction_type=CollectionViewRestriction.GROUPS,
        collection=collection
    )
    restriction.groups.add(group)
    restriction.save()

    group.user_set.add(user)
