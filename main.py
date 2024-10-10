import os
import shutil
import pytest
from utils.HandleLogs import handle


if __name__ == "__main__":
    pytest.main()
    #shutil.copy('./environment.xml','./reports/temp')
    #os.system("allure serve ./reports/temp")