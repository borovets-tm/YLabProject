from uuid import UUID

from httpx import AsyncClient, Response

from menu_app.main import app, router


def get_client():
    async_client = AsyncClient(app=app, base_url='http://test')
    try:
        yield async_client
    finally:
        async_client.aclose()


class TestReverseClient:
    def __init__(self, client=get_client):
        self.client = client
        self.routers = router

    # async def __call__(self) -> AsyncIterator[AsyncClient]:
    #     self.client: AsyncClient = AsyncClient(app=app)
    #     async with self.client as session:
    #         yield session

    async def reverse(self, url_name: str, **url_path) -> str:
        return self.routers.url_path_for(url_name, **url_path)

    async def get(self, url_name: str, **url_path):
        url = await self.reverse(url_name, **url_path)
        async with self.client() as client:
            return await client.get(url)

    async def post(self, url_name: str, data: dict, **url_path):
        url = await self.reverse(url_name, **url_path)
        async with self.client() as client:
            return await client.post(url, json=data)

    async def patch(self, url_name: str, data: dict, **url_path):
        url = await self.reverse(url_name, **url_path)
        async with self.client() as client:
            return await client.patch(url, json=data)

    async def delete(self, url_name: str, **url_path):
        url = await self.reverse(url_name, **url_path)
        async with self.client() as client:
            return await client.delete(url)


class BaseTest:
    menu_id: UUID | None = None
    submenu_id: UUID | None = None
    dish_id: UUID | None = None
    title_menu: str = 'Test menu 1'
    description_menu: str = 'Description test menu 1'
    title_submenu: str = 'Test submenu 1'
    description_submenu: str = 'Description test submenu 1'
    title_dish: str = 'Test dish 1'
    description_dish: str = 'Description test dish 1'
    price_dish: str = '12.50'

    def __init__(self):
        self.reverse = TestReverseClient()
        self.update_title_menu = 'Updated test menu 1'
        self.update_description_menu = 'Updated description test menu 1'
        self.update_title_submenu = 'Updated test submenu 1'
        self.update_description_submenu = (
            'Updated description test submenu 1'
        )
        self.update_title_dish = 'Updated test dish 1'
        self.update_description_dish = 'Updated description test dish 1'
        self.update_price_dish = '14.50'
        self.submenus_count = 0
        self.dishes_count = 0

    @classmethod
    async def set_id(
            cls,
            menu_id: UUID | None = None,
            submenu_id: UUID | None = None,
            dish_id: UUID | None = None
    ):
        if menu_id:
            cls.menu_id = menu_id
        if submenu_id:
            cls.submenu_id = submenu_id
        if dish_id:
            cls.dish_id = dish_id

    async def create_test(
            self,
            url_name: str,
            data: dict,
            **url_path
    ) -> Response:
        return await self.reverse.post(url_name, data, **url_path)

    async def retrieve_test(self, url_name: str, **url_path) -> Response:
        return await self.reverse.get(url_name=url_name, **url_path)

    async def update_test(
            self,
            url_name: str,
            data: dict,
            **url_path
    ) -> Response:
        return await self.reverse.patch(url_name, data, **url_path)

    async def delete_test(self, url_name: str, **url_path) -> Response:
        return await self.reverse.delete(url_name=url_name, **url_path)
