"""Модуль фоновых задач, обрабатываемых Celery."""
from uuid import UUID

from openpyxl import Workbook, load_workbook
from sqlalchemy import delete

from menu_app.config import config
from menu_app.models import Dish, Menu, Submenu
from menu_app.worker import SyncSessionLocal, celery

fields_menu = ('id', 'title', 'description')
fields_submenu = ('menu_id', 'id', 'title', 'description')
fields_dish = (
    'submenu_id',
    'id',
    'title',
    'description',
    'price',
    'discount'
)


@celery.task
def update_db_from_excel(
        wb: Workbook = load_workbook(config.BASE_DIR / 'admin/Menu.xlsx')
) -> None:
    """
    Функция обновляет данные в базе из excel файла в фоновом режиме каждые 15\
     секунд.

    :return: None.
    """
    try:
        sheet = wb.active
        data_list: list = []
        id_dict: dict = {
            'menu': [],
            'submenu': [],
            'dish': []
        }
        menu_id: UUID | None = None
        submenu_id: UUID | None = None
        for i in range(1, sheet.max_row + 1):
            data_entity = []
            for j in range(1, sheet.max_column + 1):
                cell_obj = sheet.cell(row=i, column=j).value
                if cell_obj:
                    if j in [1, 2, 3]:
                        try:
                            cell_obj = UUID(cell_obj)
                            if j == 1:
                                menu_id = cell_obj
                                id_dict['menu'].append(cell_obj)
                            elif j == 2:
                                submenu_id = cell_obj
                                id_dict['submenu'].append(cell_obj)
                            else:
                                id_dict['dish'].append(cell_obj)
                        except ValueError:
                            pass
                else:
                    if j == 1:
                        cell_obj = menu_id
                    elif j == 2:
                        cell_obj = submenu_id
                    else:
                        continue
                data_entity.append(cell_obj)
            data_list.append(data_entity)
        menu_data_list = list(filter(lambda x: len(x) == 3, data_list))
        submenu_data_list = list(filter(lambda x: len(x) == 4, data_list))
        dish_data_list = list(filter(lambda x: len(x) > 4, data_list))
        menu_data_list = [
            Menu(**dict(zip(fields_menu, data))) for data in menu_data_list
        ]
        submenu_data_list = [
            Submenu(**dict(zip(fields_submenu, data)))
            for data in submenu_data_list
        ]
        dish_data_list = [
            Dish(**dict(zip(fields_dish, data[1:]))) for data in dish_data_list
        ]
        obj_list = menu_data_list + submenu_data_list + dish_data_list
        with SyncSessionLocal() as db:
            for obj in obj_list:
                db.merge(obj)
            query_menu = delete(Menu).filter(Menu.id.not_in(id_dict['menu']))
            query_submenu = delete(Submenu).filter(
                Submenu.id.not_in(id_dict['submenu'])
            )
            query_dish = delete(Dish).filter(Dish.id.not_in(id_dict['dish']))
            db.execute(query_menu)
            db.execute(query_submenu)
            db.execute(query_dish)
            db.commit()
    except FileNotFoundError:
        pass
