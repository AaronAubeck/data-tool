import pytest

import sys

sys.path.insert(0, '/opt/development/scripts')
import main


@pytest.fixture
def fixture_database():
    with open("/opt/testing/tests/mock_database.csv", "r") as csv_file:
        database = pd.read_csv(csv_file)
    return database
