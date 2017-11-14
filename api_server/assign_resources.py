from . import api

from .api_resources.UserLogin import UserLogin
from .api_resources.UserSettings import UserSettings
from .api_resources.UserRegister import UserRegister
from .api_resources.CarPools import CarPools
from .api_resources.Reservations import Reservations
from .api_resources.Offers import Offers

api.add_resource(UserLogin, "/api/login")
api.add_resource(UserRegister, "/api/reg")
api.add_resource(UserSettings, "/api/settings")
api.add_resource(CarPools, "/api/carPools")
# api.add_resource(Reservation, "/api/reservations")
# api.add_resource(Offer, "/api/offers")
