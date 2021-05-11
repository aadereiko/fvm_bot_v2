from telegram import Bot
import os

# local
# is_local = True
# fvm_token = "1369098570:AAEGEKqSjXgHXrX3Gkk0_YmV0QOnuiHEtko"

# prod
is_local = False
fvm_token = "1824615819:AAFu0XQWQJHDgYu2cYt7SH1tKdPlzCZUxF4"
PORT = int(os.environ.get('PORT', '8443'))

marika_id = "399887481"
ader_id = "323428638"
sasha_id = "246505267"
rost_id = "341321543"

bot = Bot(fvm_token)