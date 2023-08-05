from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache

VIEW_CACHE_SECONDS=60
EDIT_CACHE_SECONDS=60


def user_can_alter_comment(user, comment):
    return user.is_superuser or user == comment.author or user_is_workgroup_manager(user, comment.post.workgroup)


def user_can_alter_post(user, post):
    return user.is_superuser or user == post.author or user_is_workgroup_manager(user, post.workgroup)


def user_can_view(user, item):
    """Can the user view the item?"""
    if user.is_superuser:
        return True
    if item.__class__ == User:              # -- Sometimes duck-typing fails --
        return user == item                 # A user can edit their own details

    if user.is_anonymous():
        user_key = "anonymous"
    else:
        user_key = str(user.id)

    # If the item was modified in the last 15 seconds, don't use cache
    if hasattr(item, "was_modified_very_recently") and item.was_modified_very_recently():
        can_use_cache = False
    else:
        can_use_cache = True

    cached_can_view = cache.get('user_can_view_%s|%s' % (user_key, str(item.id)))
    if can_use_cache and cached_can_view is not None:
        return cached_can_view

    _can_view = False

    _can_view = item.can_view(user)
    cache.set('user_can_view_%s|%s' % (str(user.id), str(item.id)), _can_view, VIEW_CACHE_SECONDS)
    return _can_view


def user_can_edit(user, item):
    """Can the user edit the item?"""
    # Superusers can edit everything
    if user.is_superuser:
        return True
    # Anonymous users can edit nothing
    if user.is_anonymous():
        return False
    # A user can edit their own details
    if item.__class__ == User:              # -- Sometimes duck-typing fails --
        return user == item

    if hasattr(item, "was_modified_very_recently") and item.was_modified_very_recently():
        # If the item was modified in the last 15 seconds, don't use cache
        can_use_cache = False
    else:
        can_use_cache = True

    cached_can_edit = cache.get('user_can_edit_%s|%s' % (str(user.id), str(item.id)))
    if can_use_cache and cached_can_edit is not None:
        return cached_can_edit

    _can_edit = False

    if not user_can_view(user, item):
        _can_edit = False
    else:
        _can_edit = item.can_edit(user)
    cache.set('user_can_edit_%s|%s' % (str(user.id), str(item.id)), _can_edit, VIEW_CACHE_SECONDS)

    return _can_edit


def user_is_editor(user, workgroup=None):
    if user.is_superuser:
        return True
    elif workgroup is None:
        return user.submitter_in.count() > 0 or user.steward_in.count() > 0
    else:
        return user.submitter_in.filter(workgroup=workgroup).exists() or \
            user.steward_in.filter(workgroup=workgroup).exists()


def user_is_registrar(user, ra=None):
    if user.is_superuser:
        return True
    elif ra is None:
        return user.registrar_in.count() > 0
    else:
        return user in ra.registrars.all()


def user_is_workgroup_manager(user, workgroup=None):
    if user.is_superuser:
        return True
    elif workgroup is None:
        return user.workgroup_manager_in.count() > 0
    else:
        return user in workgroup.managers.all()


def user_can_change_status(user, item):
    """Can the user change the status of the item?"""

    # Cache if the user can view as we use it a few times.
    can_view = user_can_view(user, item)
    if not can_view:
        return False
    if user.is_superuser:
        return True
    # TODO: restrict to only those registration authorities of that items based
    # on the items workgroup, unless the item is visible to the user.
    from aristotle_mdr.models import WORKGROUP_OWNERSHIP
    if item.readyToReview and user.registrar_in.count() > 0:
        if item.workgroup.ownership == WORKGROUP_OWNERSHIP.authority:
            return any(
                (user in ra.registrars.all()
                    for ra in item.workgroup.registrationAuthorities.all())
            )
        else:
            return True
    return False


def user_in_workgroup(user, wg):
    if user.is_superuser:
        return True
    return user in wg.members


def user_can_move_any_workgroup(user):
    """Checks if a user can move an item from any of their workgroups"""
    workgroup_change_access = getattr(settings, 'ARISTOTLE_SETTINGS', {}).get('WORKGROUP_CHANGES', [])

    if user.is_superuser:
        return True
    if 'admin' in workgroup_change_access and user.is_staff:
        return True
    if 'manager' in workgroup_change_access and user.profile.is_workgroup_manager():
        return True
    if 'submitter' in workgroup_change_access and user.submitter_in.exists():
        return True

    return False


def user_can_add_or_remove_workgroup(user, workgroup):
    workgroup_change_access = getattr(settings, 'ARISTOTLE_SETTINGS', {}).get('WORKGROUP_CHANGES', [])

    if user.is_superuser:
        return True
    if 'admin' in workgroup_change_access and user.is_staff:
        return True
    if 'manager' in workgroup_change_access and user in workgroup.managers.all():
        return True
    if 'submitter' in workgroup_change_access and user in workgroup.submitters.all():
        return True
    return False


def user_can_remove_from_workgroup(user, workgroup):
    return user_can_add_or_remove_workgroup(user, workgroup)


def user_can_move_to_workgroup(user, workgroup):
    return user_can_add_or_remove_workgroup(user, workgroup)


def user_can_move_between_workgroups(user, workgroup_a, workgroup_b):
    """checks if a user can move an item from A to B"""
    return user_can_remove_from_workgroup(user, workgroup_a) and user_can_move_to_workgroup(user, workgroup_b)
