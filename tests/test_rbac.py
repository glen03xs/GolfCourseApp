import pytest

from src.rbac import (
    PermissionDeniedError,
    StaffUser,
    UserAlreadyExistsError,
    UserDirectory,
)


def test_it_admin_can_assign_role() -> None:
    directory = UserDirectory()
    admin = StaffUser("glen@golf.com", "Glen", "IT_ADMIN")
    staff = StaffUser("alex@golf.com", "Alex", "PRO_SHOP")

    directory.add_user(admin)
    directory.add_user(staff)

    directory.assign_role(admin, "alex@golf.com", "MANAGER")

    assert staff.role == "MANAGER"
    assert staff.can("edit_sops") is True


def test_non_admin_cannot_assign_role() -> None:
    directory = UserDirectory()
    manager = StaffUser("sam@golf.com", "Sam", "MANAGER")
    staff = StaffUser("alex@golf.com", "Alex", "PRO_SHOP")

    directory.add_user(manager)
    directory.add_user(staff)

    with pytest.raises(PermissionDeniedError):
        directory.assign_role(manager, "alex@golf.com", "IT_ADMIN")


def test_duplicate_email_raises_error() -> None:
    directory = UserDirectory()
    user1 = StaffUser("alex@golf.com", "Alex", "PRO_SHOP")
    user2 = StaffUser("alex@golf.com", "Alex Duplicate", "MANAGER")

    directory.add_user(user1)

    with pytest.raises(UserAlreadyExistsError):
        directory.add_user(user2)


def test_deactivated_user_loses_all_permissions() -> None:
    directory = UserDirectory()
    admin = StaffUser("glen@golf.com", "Glen", "IT_ADMIN")
    manager = StaffUser("sam@golf.com", "Sam", "MANAGER")

    directory.add_user(admin)
    directory.add_user(manager)

    directory.deactivate_user(admin, "sam@golf.com")

    assert manager.is_active is False
    assert manager.can("view_sops") is False
    assert manager.can("edit_sops") is False


def test_list_by_role_excludes_inactive_users() -> None:
    directory = UserDirectory()
    admin = StaffUser("glen@golf.com", "Glen", "IT_ADMIN")
    pro1 = StaffUser("alex@golf.com", "Alex", "PRO_SHOP")
    pro2 = StaffUser("jamie@golf.com", "Jamie", "PRO_SHOP")

    directory.add_user(admin)
    directory.add_user(pro1)
    directory.add_user(pro2)
    directory.deactivate_user(admin, "jamie@golf.com")

    active_pro_shop = directory.list_by_role("PRO_SHOP")

    assert len(active_pro_shop) == 1
    assert active_pro_shop[0].email == "alex@golf.com"


def test_invalid_role_raises_value_error() -> None:
    directory = UserDirectory()
    admin = StaffUser("glen@golf.com", "Glen", "IT_ADMIN")
    staff = StaffUser("alex@golf.com", "Alex", "PRO_SHOP")

    directory.add_user(admin)
    directory.add_user(staff)

    with pytest.raises(ValueError):
        directory.assign_role(admin, "alex@golf.com", "INTERN")
