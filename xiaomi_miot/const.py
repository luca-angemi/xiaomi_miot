"""Constants of the Xiaomi AirFryer component."""
from datetime import timedelta

DEFAULT_NAME = "Xiaomi AirFryer"
DOMAIN = "xiaomi_miot"
DOMAINS = ["sensor", "switch", "select", "button"]
DATA_KEY = "xiaomi_airfryer_data"
DATA_STATE = "state"
DATA_DEVICE = "device"

CONF_MODEL = "model"
CONF_MAC = "mac"

MODEL_FRYER_MAF10A = "careli.fryer.maf10a"
MODEL_FRYER_MAF05A = "careli.fryer.maf05a"

MODELS_CARELI = [
    MODEL_FRYER_MAF10A,
    MODEL_FRYER_MAF05A
]

MODELS_ALL_DEVICES = MODELS_CARELI

ATTR_FOOD_QUANTY = "food_quanty"
ATTR_MODEL = "model"
ATTR_MODE = "mode"
ATTR_TIME = "time"
ATTR_TARGET_TIME = "target_time"
ATTR_TARGET_TEMPERATURE = "target_temperature"
ATTR_RECIPE_ID = "recipe_id"

SUCCESS = ["ok"]

DEFAULT_SCAN_INTERVAL = 30
SCAN_INTERVAL = timedelta(seconds=30)

SERVICE_START = "start"
SERVICE_STOP = "stop"
SERVICE_PAUSE = "pause"
SERVICE_START_CUSTOM = "start_custom"
SERVICE_RESUME = "resume"
SERVICE_APPOINT_TIME = "appoint_time"
SERVICE_RECIPE_ID = "recipe_id"
SERVICE_FOOD_QUANTY = "food_quanty"
SERVICE_TARGET_TIME = "target_time"
SERVICE_TARGET_TEMPERATURE = "target_temperature"
