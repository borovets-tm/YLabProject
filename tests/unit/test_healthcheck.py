import dotenv
import pytest

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


@pytest.fixture()
def test_change_db_on_test():
    dotenv.set_key(dotenv_file, 'TEST', '1')
    test_value = dotenv.get_key(dotenv_file, 'TEST')
    assert test_value == '1'


@pytest.mark.order('last')
@pytest.mark.asyncio
async def test_clear_cache_after_test():
    dotenv.set_key(dotenv_file, 'TEST', '0')
    test_value = dotenv.get_key(dotenv_file, 'TEST')
    assert test_value == '0'
