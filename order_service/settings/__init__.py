from order_service.settings.common import *  # NoQA: F401

PHASE = config("PHASE", "local")

if PHASE == "develop":
    from order_service.settings.develop import *  # NoQA: F401
elif PHASE == "staging":
    from order_service.settings.staging import *  # NoQA: F401
elif PHASE == "production":
    from order_service.settings.production import *  # NoQA: F401
else:
    raise Exception("PHASE environment variable is not set properly.")