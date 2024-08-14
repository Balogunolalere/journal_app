from deta import Deta
from app.core.config import settings

deta = Deta(settings.DETA_PROJECT_KEY)
journal_base = deta.Base("journal_entries")
user_base = deta.Base("journal_users")