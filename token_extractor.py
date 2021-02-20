import os
try: 
    f = open("token.secret", "r")
    token = f.read()
except:
    token = os.environ["BOT_TOKEN"]
    # token = "1519348433:AAHa_065sbf3b32krSINHs5saDC_4M2kD8Q"