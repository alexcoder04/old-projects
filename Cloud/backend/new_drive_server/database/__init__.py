from .users import UsersDataBase
from .logins import LoginsDataBase
from .shared_files import SharedFilesdataBase
from .opendb import OpenDB

db = UsersDataBase()
logins_db = LoginsDataBase()
shared_files_db = SharedFilesdataBase()
