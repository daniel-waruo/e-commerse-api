from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from accounts.models import User
from business.authorization.models import Department, StaffUser


def create_staff_user(user_id: int, staff_type: int, department_ids: list):
    """
    This function creates a staff user and sets the staff_type and departments
    :param user_id:
    :param staff_type:
    :param department_ids:
    :return: staff
    """
    # create a staff user instance
    staff = StaffUser(
        user_id=user_id,
        staff_type=staff_type
    )
    # save staff information
    staff.save()
    # set the departments for the staff
    staff.departments.set(department_ids)
    return staff


def set_department_manager_perms(user_id: int, department_ids: list = None):
    """
    This function sets the permission of a department manager to a user
    :param user_id:
    :param department_ids:
    :return:user
    """
    # get all users that are related to the staff user
    users = get_user_model().objects.select_related("staffuser")
    # check if the user exist in the group of users
    if users.filter(id=user_id):
        # get the staff user model instance
        staff_user: StaffUser = users.get(id=user_id).staffuser
        if staff_user.staff_type < 1:
            # set the staff type
            staff_user.staff_type = 1
            # save the information to the database
            staff_user.save()
        # if department ids set the departments for the staff user
        if department_ids:
            # set the departments to the staff user
            staff_user.departments.set([department_ids])
    # if the user if not in this group of users create staff user instance
    else:
        # assert department_ids necessary for creating a new staff user instance
        assert department_ids, "Department Ids Must be set as the user is not yet a staff"
        # create a staff user
        create_staff_user(user_id, 1, department_ids)
    # get user object
    user: User = get_user_model().objects.get(id=user_id)

    # set the permissions for a user in a department
    departmental_perms = get_valid_permission_ids(user_id)
    # get the permission ids of a department manager as
    department_manager_perms = list(
        map(
            lambda permission: permission.id,
            Permission.objects.filter(
                codename__in=['set_permissions', 'include_department']
            )
        ))
    # raise Exception(str(type(department_manager_perms)))
    # get all the perms allowed for a departmental manager
    perms = list({*departmental_perms, *department_manager_perms})
    # set the perms of a departments manager
    user.user_permissions.set(perms)
    return user


def set_general_manager_perms(user_id: int, department_ids: list = None):
    """
    This function sets the permission of a department manager to a user
    :param user_id:
    :param department_ids:
    :return:user
    """
    # get all users that are related to the staff user
    users = get_user_model().objects.select_related("staffuser")
    # check if the user exist in the group of users
    if users.filter(id=user_id):
        # get the staff user
        staff_user: StaffUser = users.get(id=user_id).staffuser
        if staff_user.staff_type < 2:
            # set the staff type
            staff_user.staff_type = 2
            # save the information to the database
            staff_user.save()
        # if department ids set the departments for the staff user
        if department_ids:
            # set the departments to the staff user
            staff_user.departments.set([department_ids])
    # if the user if not in this group of users create staff user instance
    else:
        # assert department_ids necessary for creating a new staff user instance
        assert department_ids, "Department Ids Must be set as the user is not yet a staff"
        # create a staff user
        create_staff_user(user_id, 1, department_ids)
    # get user object
    user: User = get_user_model().objects.get(id=user_id)

    # set the permissions for a user in a department
    departmental_perms = get_valid_permission_ids(user_id)
    # get the permission ids of a general manager as
    general_manager_perms = list(
        map(
            lambda permission: permission.id,
            Permission.objects.filter(
                codename__in=['set_permissions', 'include_department', 'manage_department_manager']
            )
        ))
    # get all the perms allowed for a departmental manager
    perms = list({*departmental_perms, *general_manager_perms})
    # set the perms of a departments manager
    user.user_permissions.set(perms)
    return user


# return all department objects
def get_all_departments():
    return Department.objects.all()


# get all department objects ids
def get_all_department_ids():
    return list(map(lambda department: department.id, get_all_departments()))


# get all the departments instances a user is enrolled to
def get_user_departments(user_id):
    return Department.objects.filter(staffuser__user_id=user_id)


# get all the department data
def get_user_departments_data(user_id):
    pass


# get all the department instances ids belonging to a user
def get_user_department_ids(user_id):
    return list(map(lambda department: department.id, get_user_departments(user_id)))


# get all the permissions belonging to a department
def get_department_permissions(departments):
    app_labels = list(map(lambda department: department.app_label, departments))
    return Permission.objects.filter(content_type__app_label__in=app_labels)


def get_department_permission_ids(departments):
    return list(map(
        lambda department: department.id,
        get_department_permissions(departments)
    ))


# get all valid user permissions for a user
def get_valid_user_permissions(user_id):
    departments = get_user_departments(user_id)
    return get_department_permissions(departments)


# get all valid user permission ids for a particular user
def get_valid_permission_ids(user_id):
    permissions = get_valid_user_permissions(user_id)
    return list(map(lambda permission: permission.id, permissions))


def validate_permissions(view_user_id, user_id, permissions):
    """
    Checks whether the user giving the permissions has that authority
    Checks whether the user permissions have been set within user valid permissions
    :param: view_user_id:
    :param user_id:
    :param permissions:
    :return:type::tuple permissions,is_valid
    """
    # make sure view user assigning permissions in his own range
    for permission in permissions:
        # make sure the user giving the permissions are within the users jurisdiction
        if permission not in get_valid_permission_ids(view_user_id):
            return permissions, False
        # make sure the user is given valid permissions to the number of departments
        if permission not in get_valid_permission_ids(user_id):
            return permissions, False
    # make sure the permissions set to a user are within their department
    return permissions, True


def validate_departments(user_id, departments):
    """
    Make sure the manager has set a department within his jurisdiction
    :param user_id:
    :param departments:
    :return:type::tuple departments,is_valid
    """
    # make sure view user assigning permissions in his own range
    for department in departments:
        if department not in get_user_department_ids(user_id):
            return departments, False
    # make sure the permissions set to a user are within their department
    return departments, True
