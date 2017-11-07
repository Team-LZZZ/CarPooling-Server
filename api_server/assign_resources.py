from . import api

from .api_resources.UserLogin import UserLogin
from .api_resources.UserRegister import UserRegister
from .api_resources.UpdateSettings import UpdateSettings
from .api_resources.CancelReservation import CancelReservation
from .api_resources.ListAllCarPools import ListAllCarPools
from .api_resources.GetStates import GetStates
from .api_resources.MakeReservation import MakeReservation
from .api_resources.MakeOffer import MakeOffer
from .api_resources.GetCarPools import GetCarPools

api.add_resource(UserLogin, "/carPooling/login")
api.add_resource(UserRegister, "/carPooling/reg")
api.add_resource(UpdateSettings, "/carPooling/updateSettings")
api.add_resource(ListAllCarPools, "/carPooling/allCarPools")
# api.add_resource(GetStates, "/carPooling/states")
# api.add_resource(MakeReservation, "/carPooling/makeReservation")
# api.add_resource(MakeOffer, "/carPooling/makeOffer")
# api.add_resource(GetCarPools, "/carPooling/searchCarPools")
# api.add_resource(CancelReservation, "/carPooling/cancelReservation")
