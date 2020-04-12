from django.contrib.admin.utils import quote, capfirst
from django.utils.translation import gettext_lazy as _

from wagtail.contrib.modeladmin.helpers import (
    AdminURLHelper as AdminURLHelperBase,
    PermissionHelper as PermissionHelperBase,
    ButtonHelper as ButtonHelperBase
)


class AdminURLHelper(AdminURLHelperBase):
    """ Custom AdminURLHelper """


class PermissionHelper(PermissionHelperBase):
    """ Custom PermissionHelper """

    def user_can(self, codename, user, obj=None):
        perm_codename = self.get_perm_codename(codename)
        return self.user_has_specific_permission(user, perm_codename)

    def can_view_other(self, user):
        return self.user_can('viewother', user)

    def can_change_other(self, user):
        return self.user_can('changeother', user)

    def is_owner(self, user, obj):
        return obj.creator == user

    def is_owner_manager(self, user, obj):
        creator_manager_position = obj.creator.person.employee.position.get_ancestors(ascending=True)[0]
        user_position = user.person.employee.position
        return user_position == creator_manager_position

    def user_can_edit_obj(self, user, obj):
        return self.user_can('change', user)

    def user_can_inspect_obj(self, user, obj):
        return self.inspect_view_enabled and self.user_has_any_permissions(user)


class ButtonHelper(ButtonHelperBase):
    """ Custom ButtonHelper """

    def create_custom_button(self, codename, pk=None, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.default_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': self.url_helper.get_action_url(codename, quote(pk)),
            'label': capfirst(_(codename.replace('_', ' '))),
            'classname': cn,
            'title': _('%s this %s') % (codename, self.verbose_name,),
        }
