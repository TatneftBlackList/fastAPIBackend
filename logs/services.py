from typing import List

from logs.repositories import UserRequestLogRepository
from sqlalchemy.ext.asyncio import AsyncSession
from permissions.permission_verification import PermissionVerification
from logs.models import UserRequestLogModel
from logs.schemas import LogsSchema, UsersSchemaResponse


class UserRequestLogService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_request_repository = UserRequestLogRepository(db)
        self.permission_verification = PermissionVerification(db)

    async def get_logs(self, current_user: dict):
        if await self.permission_verification.get_verification(current_user['permissions']):
            logs = await self.user_request_repository.get_logs()
            logs_list = []

            for log in logs:

                logs_list.append(await self.__convert_to_schema(log))

            return logs_list

    async def get_log(self, current_user: dict, log_id: int):
        if await self.permission_verification.get_verification(current_user['permissions']):
            log = await self.user_request_repository.get_log(log_id)
            return await self.__convert_to_schema(log)

    async def __convert_to_schema(self, user_req_model: UserRequestLogModel):
        return LogsSchema(
            id=user_req_model.id,
            user=UsersSchemaResponse(
                id=user_req_model.user.id,
                job_number=user_req_model.user.user_rel.job_number,
                first_name=user_req_model.user.user_rel.first_name,
                last_name=user_req_model.user.user_rel.last_name,
            ),
            path=user_req_model.path,
            method=user_req_model.method,
            timestamp=user_req_model.timestamp,
            response_status=user_req_model.response_status,
        )
