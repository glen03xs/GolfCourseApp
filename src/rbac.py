from dataclasses import dataclass


# 1. Custom Exceptions
class UserAlreadyExistsError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


# 2. Role Permissions Mapping
ROLE_PERMISSIONS: dict[str, set[str]] = {
    "IT_ADMIN": {"manage_users", "edit_sops", "view_sops", "update_website"},
    "MANAGER": {"edit_sops", "view_sops", "manage_bookings", "update_website"},
    "PRO_SHOP": {"view_sops", "manage_bookings"},
}


# 3. StaffUser Dataclass
@dataclass
class StaffUser:
    email: str
    full_name: str
    role: str
    is_active: bool = True

    def can(self, permission: str) -> bool:
        if not self.is_active:
            return False
        allowed_permissions = ROLE_PERMISSIONS.get(self.role, set())
        return permission in allowed_permissions

    def deactivate(self) -> None:
        self.is_active = False


# 4. UserDirectory Manager (Day 2)
class UserDirectory:
    def __init__(self) -> None:
        # Dictionary storing users by email: {"glen@golf.com": StaffUser(...)}
        self.users: dict[str, StaffUser] = {}

    def add_user(self, user: StaffUser) -> None:
        if user.email in self.users:
            raise UserAlreadyExistsError(f"User {user.email} already exists")
        self.users[user.email] = user

    def assign_role(self, actor: StaffUser, target_email: str, new_role: str) -> None:
        if not actor.can("manage_users"):
            raise PermissionDeniedError(f"{actor.email} cannot manage users")
        if target_email not in self.users:
            raise KeyError(f"User {target_email} not found")
        if new_role not in ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {new_role}")

        self.users[target_email].role = new_role

    def deactivate_user(self, actor: StaffUser, target_email: str) -> None:
        if not actor.can("manage_users"):
            raise PermissionDeniedError(f"{actor.email} cannot manage users")
        if target_email not in self.users:
            raise KeyError(f"User {target_email} not found")

        self.users[target_email].deactivate()

    def list_by_role(self, role: str) -> list[StaffUser]:
        return [u for u in self.users.values() if u.is_active and u.role == role]
