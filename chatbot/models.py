from pony.orm import Database, Required, Json

from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """Состояние пользователя внутри сценаярия"""
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context=Required(Json)

class Registration(db.Entity):
    """Заявка на регистрацию"""
    sity_of_departyre = Required(str)
    sity_of_arrival = Required(str)
    selected_flight_date = Required(str)


db.generate_mapping(create_tables=True)

