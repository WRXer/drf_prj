import stripe
import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule


class PaymentService:
    def __init__(self):
        stripe.api_key = "sk_test_51NY2NFC6FmNGzKCpcrYZUQyW69kGtmhRUo1WIJ1oeYNOp3q9uHeG6NwEUTxNU5nnbpGhscWdfKf8PgbUBeRFfWSf00AFcDijqW"

    def create_payment(self, amount, currency):
        amount = amount  # сумма в центах (например, 10.00 долларов США)
        currency = currency  # валюта платежа (например, доллар США)
        payment_method_types = ["card"]  # метод оплаты (например, "card" для оплаты картой)

        try:
            # Создаем сессию чекаута
            session = stripe.checkout.Session.create(
                payment_method_types=payment_method_types,
                line_items=[{
                    "price_data": {
                        "currency": currency,
                        "unit_amount": amount,
                        "product_data": {
                            "name": "Тестовый продукт",  # Название продукта
                        },
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url="https://example.com/success",  # URL для перенаправления после успешной оплаты
            )

            # Получаем идентификатор сессии чекаута (session_id)
            session = session.url
            return session
        except stripe.error.StripeError as e:
            print(f"Error: {e}")
            return None


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=1,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,  # we created this above.
        name='block_inactive_users',  # simply describes this periodic task.
        task='main.tasks.block_inactive_users',  # name of task.
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
