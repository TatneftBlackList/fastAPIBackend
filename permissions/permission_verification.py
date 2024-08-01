from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from permissions.enums import PermissionEnums
from permissions.repositories import PermissionRepository


class PermissionVerification:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.permission_repository = PermissionRepository(db)

    async def get_verification(self, permissions: []):
        if [permission for permission in permissions if permission == PermissionEnums.READ.name]:
            return True
        raise HTTPException(
            detail="User does not have permission",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    async def post_verification(self, permissions: []):
        if [permission for permission in permissions if permission == PermissionEnums.CREATE.name]:
            return True
        raise HTTPException(
            detail="User does not have permission",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    async def put_patch_verification(self, permissions: []):
        if [permission for permission in permissions if permission == PermissionEnums.UPDATE.name]:
            return True
        raise HTTPException(
            detail="User does not have permission",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    async def delete_verification(self, permissions: []):
        if [permission for permission in permissions if permission == PermissionEnums.DELETE.name]:
            return True
        raise HTTPException(
            detail="User does not have permission",
            status_code=status.HTTP_403_FORBIDDEN,
        )
