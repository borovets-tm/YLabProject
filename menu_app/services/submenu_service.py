"""Модуль сервисного слоя для модели Submenu."""
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from menu_app.repositories.submenu_repository import SubmenuRepository, repository
from menu_app.schemas.submenu import Submenu, SubmenuCreate

from .base_service import BaseService


class SubmenuService(BaseService):
    """Модель сервисных методов для под-меню."""

    def __init__(self) -> None:
        """Инициализация класса с указанием слоя репозитория."""
        super().__init__()
        self.repository: SubmenuRepository = repository

    async def get_list(
            self,
            db: AsyncSession, path_params: dict
    ) -> list[Submenu]:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса списка под-меню, устанавливает кэш и передает данные в роутер.

        :param db: Экземпляром сеанса базы данных.
        :param path_params: Словарь со списком параметров пути.
        :return: Список под-меню.
        """
        s: dict = await self.get_lazy_s(path_params)
        result = await self.get_cache(self.get_list_submenu % s)
        if not result:
            result = await self.repository.get_list(db)
            await self.set_cache(self.get_list_submenu % s, result)
        return result

    async def get(
            self,
            db: AsyncSession,
            submenu_id: UUID,
            path_params: dict
    ) -> Submenu:
        """
        Метод проверяет наличие кэша запроса. При положительном результате\
        возвращает полученный кэш, в противном случае получает результат\
        запроса экземпляра под-меню, устанавливает кэш и передает данные в\
        роутер.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор под-меню.
        :param path_params: Словарь со списком параметров пути.
        :return: Экземпляр модели.
        """
        s: dict = await self.get_lazy_s(path_params)
        result = await self.get_cache(self.get_submenu % s)
        if not result:
            result = await self.repository.get(db, submenu_id)
            await self.set_cache(self.get_submenu % s, result)
        return result

    async def create(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            menu_id: UUID,
            path_params: dict
    ) -> Submenu:
        """
        Метод работает с методом создания нового экземпляра под-меню, удаляя из\
        кэша записи результатов запросов: получения списков меню, под-меню;\
        информации о меню, связанного с под-меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для создания нового экземпляра.
        :param menu_id: Идентификатор меню, к которому относится под-меню.
        :param path_params: Словарь со списком параметров пути.
        :return: Экземпляр созданного под-меню.
        """
        s: dict = await self.get_lazy_s(path_params)
        await self.delete_cache(
            [
                self.get_list_menu,
                self.get_menu % s,
                self.get_list_submenu % s,
            ]
        )
        return await self.repository.create(db, data, menu_id)

    async def update(
            self,
            db: AsyncSession,
            data: SubmenuCreate,
            submenu_id: UUID,
            path_params: dict
    ) -> Submenu:
        """
        Метод удаляет из кэша записи запросов списка под-меню и обновляемого\
        под-меню.

        :param db: Экземпляром сеанса базы данных.
        :param data: Данные для обновления.
        :param submenu_id: Идентификатор под-меню.
        :param path_params: Словарь со списком параметров пути.
        :return: Экземпляр под-меню с обновленными данными.
        """
        s: dict = await self.get_lazy_s(path_params)
        await self.delete_cache(
            [
                self.get_list_submenu % s,
                self.get_submenu % s
            ]
        )
        return await self.repository.update(db, data, submenu_id)

    async def delete(
            self,
            db: AsyncSession,
            submenu_id: UUID,
            path_params: dict
    ) -> JSONResponse:
        """
        Метод удаляет весь кэш при удалении под-меню. Удаление всего кэша\
        обусловлено тем, что удаление отдельных сегментов увеличит нагрузку\
        на запрос.

        :param db: Экземпляром сеанса базы данных.
        :param submenu_id: Идентификатор удаляемого под-меню.
        :param path_params: Словарь со списком параметров пути.
        :return: Ответ об успехе или неудачи удаления.
        """
        s: dict = await self.get_lazy_s(path_params)
        delete_list = [
            self.get_list_menu,
            self.get_menu % s,
            self.get_list_submenu % s,
            self.get_submenu % s
        ]
        delete_list += await self.get_keys_by_patterns(f'*{submenu_id}*')
        await self.delete_cache(delete_list)
        return await self.repository.remove(db, submenu_id)


service: SubmenuService = SubmenuService()
