from typing import Dict

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.service import UserService
from apps.tariffs.service import TariffService, ReceiptService

from apps.tariffs import tasks

from config.environment import SUCCEEDED, CANCELED

from utils.logger import api_logger as logger


class YoukassaWebhookAPIView(APIView):

    def post(self, request: Request):
        logger.info(f"[YOUKASSA WEBHOOK] REQUEST DATA: {request.data}")

        payment_object: Dict = request.data.get("object")
        payment_id = payment_object.get("id")
        payment_status = payment_object.get("status")

        logger.info(f"[YOUKASSA WEBHOOK] PAYMENT ID: {payment_id}")
        logger.info(f"[YOUKASSA WEBHOOK] PAYMENT STATUS: {payment_status}")

        if payment_status == SUCCEEDED:
            logger.info(f"[YOUKASSA WEBHOOK] PAYMENT SUCCESS! ({payment_id})")
            tasks.send_payment_success.apply_async(
                args=(payment_id, payment_object),
            )
            
        else:
            logger.info(f"[YOUKASSA WEBHOOK] Error, another status = {payment_status} ({payment_id})")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_200_OK)