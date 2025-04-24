from typing import List
from asgiref.sync import sync_to_async

from apps.mailing.models import Mail


class MailService:

    @staticmethod
    @sync_to_async
    def get_all_uncompleted() -> List[Mail]:
        mails = Mail.objects.filter(completed=False)
        return list(mails)

    @staticmethod
    @sync_to_async
    def mark_mail_as_completed(mail_id: int) -> Mail:
        mail = Mail.objects.get(id=mail_id)
        mail.completed = True
        mail.save()
        return mail
