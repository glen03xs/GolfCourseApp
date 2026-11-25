from dataclasses import dataclass


# 1. Custom Exceptions
class UserAlreadyExistsError(Exception):
    pass


class PermissionDeniedError(Exception):
    pass


# 2. Role Permissions Mapping (dict mapping role names to sets of permissions)
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
