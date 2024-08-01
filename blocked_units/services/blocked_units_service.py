from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import HTTPException
from blocked_units.repositories.blocked_units_repository import BlockedUnitsRepository
from blocked_units.repositories.passports_repository import PassportsRepository
from blocked_units.schemas.blocked_units import BlockedUnitSchemaRequest, BlockedUnitSchemaResponse, \
    BlockedUnitsSchemaPartialRequest
from blocked_units.models.passports import PassportsModel
from blocked_units.models.blocked_units import BlockedUnitsModel
from blocked_units.schemas.passports import PassportSchemaResponse
from company.schemas import CompanySchemaResponse
from permissions.permission_verification import PermissionVerification


class BlockedUnitsService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.blocked_units_repository = BlockedUnitsRepository(db)
        self.passports_repository = PassportsRepository(db)
        self.permission_verification = PermissionVerification(db)

    async def get_blocked_units(self, current_user: dict):
        if await self.permission_verification.get_verification(current_user['permissions']):
            blocked_units_list = []
            units = await self.blocked_units_repository.get_blocked_units()

            for unit in units:
                schema_unit = await self.__convert_to_schema(unit)
                blocked_units_list.append(schema_unit)

            return blocked_units_list

    async def add_blocked_units(self, request: BlockedUnitSchemaRequest, current_user: dict):
        if await self.permission_verification.post_verification(current_user['permissions']):
            try:
                new_passport = PassportsModel(
                    passport_number=request.passports.passport_number,
                    passport_seria=request.passports.passport_seria,
                    old_passport_seria=request.passports.old_passport_seria,
                    old_passport_number=request.passports.old_passport_number
                )

                passport = await self.passports_repository.create_passport(new_passport)

                new_blocked_unit = BlockedUnitsModel(
                    fio=request.fio,
                    passport_id=passport.id,
                    company_id=request.company_id,
                    reason=request.reason,
                )

                await self.blocked_units_repository.create_blocked_unit(new_blocked_unit)

            except IntegrityError as e:
                await self.db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Уникальное ограничение нарушено: возможно, такой паспорт уже существует.")

            unit_from_db = await self.blocked_units_repository.get_blocked_unit_by_id(new_blocked_unit.id)
            schema_blocked_unit = await self.__convert_to_schema(unit_from_db)
            return schema_blocked_unit

    async def get_unit_by_id(self, request: int, current_user: dict):
        if await self.permission_verification.get_verification(current_user['permissions']):
            unit = await self.blocked_units_repository.get_blocked_unit_by_id(request)

            if unit is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Blocked Unit not found")

            return await self.__convert_to_schema(unit)

    async def update_blocked_units(self, request: BlockedUnitSchemaRequest, blocked_unit_id: int, current_user: dict):
        if await self.permission_verification.put_patch_verification(current_user['permissions']):
            try:
                async with self.db.begin():

                    existing_blocked_units = await self.blocked_units_repository.get_blocked_unit_by_id(blocked_unit_id)

                    if existing_blocked_units is None:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blocked Unit not found")

                    existing_blocked_units.fio = request.fio
                    existing_blocked_units.company_id = request.company_id
                    existing_blocked_units.reason = request.reason

                    existing_passport = await self.passports_repository.get_passports(
                        existing_blocked_units.passport_id)

                    existing_passport_with_same_series_and_number = await self.passports_repository.get_passport_by_series_and_number(
                        request.passports.passport_seria, request.passports.passport_number
                    )

                    existing_old_passport_with_same_series_and_number = await self.passports_repository.get_old_passport_by_seria_and_number(
                        request.passports.old_passport_seria, request.passports.old_passport_number
                    )

                    if existing_passport_with_same_series_and_number or existing_old_passport_with_same_series_and_number:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Паспорт с такой серией и номером уже существует")

                    existing_passport.passport_seria = request.passports.passport_seria
                    existing_passport.passport_number = request.passports.passport_number
                    existing_passport.old_passport_seria = request.passports.old_passport_seria
                    existing_passport.old_passport_number = request.passports.old_passport_number

                    await self.passports_repository.update_passport(existing_passport)
                    await self.blocked_units_repository.update_blocked_unit(existing_blocked_units)

            except IntegrityError as e:
                await self.db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Уникальное ограничение нарушено: возможно, такой паспорт уже существует.")

            updated_unit_from_db = await self.blocked_units_repository.get_blocked_unit_by_id(existing_blocked_units.id)
            schema_blocked_unit = await self.__convert_to_schema(updated_unit_from_db)
            return schema_blocked_unit

    async def partial_update_blocked_unit(self, request: BlockedUnitsSchemaPartialRequest, blocked_unit_id: int,
                                          current_user: dict):
        if await self.permission_verification.put_patch_verification(current_user['permissions']):
            try:
                async with self.db.begin():
                    existing_blocked_units = await self.blocked_units_repository.get_blocked_unit_by_id(blocked_unit_id)

                    if existing_blocked_units is None:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blocked Unit not found")

                    if request.fio is not None:
                        existing_blocked_units.fio = request.fio

                    if request.company_id is not None:
                        existing_blocked_units.company_id = request.company_id

                    if request.reason is not None:
                        existing_blocked_units.reason = request.reason

                    if request.passports is not None:
                        existing_passport = await self.passports_repository.get_passports(
                            existing_blocked_units.passport_id)

                        if request.passports.passport_seria is not None:
                            existing_passport.passport_seria = request.passports.passport_seria

                        if request.passports.passport_number is not None:
                            existing_passport_with_same_series_and_number = await self.passports_repository.get_passport_by_number_and_seria(
                                passport_number=request.passports.passport_number,
                                passport_seria=existing_passport.passport_seria,
                                exclude_passport_id=existing_blocked_units.passport_id
                            )

                            if existing_passport_with_same_series_and_number:
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Паспорт с такой серией и номером уже существует"
                                )

                            existing_passport.passport_number = request.passports.passport_number

                        if request.passports.old_passport_seria is not None:
                            existing_passport.old_passport_seria = request.passports.old_passport_seria

                        if request.passports.old_passport_number is not None:
                            existing_old_passport_with_same_series_and_number = await self.passports_repository.get_old_passport_by_seria_and_number(
                                old_passport_number=request.passports.old_passport_number,
                                old_passport_seria=existing_passport.old_passport_seria,
                                exclude_passport_id=existing_blocked_units.passport_id
                            )

                            if existing_old_passport_with_same_series_and_number:
                                raise HTTPException(
                                    status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Старый паспорт с такой серией и номером уже существует"
                                )

                            existing_passport.old_passport_number = request.passports.old_passport_number

                        await self.passports_repository.update_passport(existing_passport)
                    await self.blocked_units_repository.update_blocked_unit(existing_blocked_units)

            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Уникальное ограничение нарушено: возможно, такой паспорт уже существует.")

            updated_unit_from_db = await self.blocked_units_repository.get_blocked_unit_by_id(existing_blocked_units.id)
            schema_blocked_unit = await self.__convert_to_schema(updated_unit_from_db)
            return schema_blocked_unit

    async def delete_blocked_unit(self, unit_id: int, current_user: dict):
        if await self.permission_verification.delete_verification(current_user['permissions']):
            existing_blocked_units = await self.blocked_units_repository.get_blocked_unit(unit_id)

            if existing_blocked_units is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Blocked Unit not found"
                )

            await self.passports_repository.delete_passport(existing_blocked_units.passport_id)
            await self.blocked_units_repository.delete_blocked_units(existing_blocked_units)

    async def __convert_to_schema(self, unit):
        blocked_unit = BlockedUnitSchemaResponse(
            id=unit.id,
            fio=unit.fio,
            passports=PassportSchemaResponse(
                id=unit.passports_rel.id,
                passport_seria=unit.passports_rel.passport_seria,
                passport_number=unit.passports_rel.passport_number,
                old_passport_number=unit.passports_rel.old_passport_number,
                old_passport_seria=unit.passports_rel.old_passport_seria,
            ),
            company=CompanySchemaResponse(
                id=unit.company_rel.id,
                name=unit.company_rel.name,
            ),
            reason=unit.reason,
            date_add_to_list=unit.date_add_to_list,
        )
        return blocked_unit
