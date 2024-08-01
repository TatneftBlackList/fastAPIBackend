from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import AuthModel
from permissions.repositories import PermissionRepository
from auth.dependencies import get_current_user
from db.session import get_session
from permissions.enums import PermissionEnums


class PermissionRequired:
    def __init__(self, permission: PermissionEnums):
        self.permission = permission

    async def __call__(self, current_user: AuthModel = Depends(get_current_user),
                       session: AsyncSession = Depends(get_session)):
        permission_repository = PermissionRepository(session)
        has_perm = await permission_repository.has_permission(current_user.user_id, self.permission)
        if not has_perm:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Пользователь не имеет разрешения {self.permission}"
            )
        return has_perm


def permission_required(permission: PermissionEnums):
    return PermissionRequired(permission)
