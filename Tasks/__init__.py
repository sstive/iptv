from .updater import Updater
from .mail_manager import MailManager


TASKS = [
    Updater(),
    MailManager()
]
