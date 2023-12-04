import stripe
from django.shortcuts import redirect

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_and_save_link_to_pay(obj):

    product = stripe.Product.create(name=obj.name)

    price = stripe.Price.create(
        unit_amount=obj.price,
        currency="usd",
        recurring={"interval": "month"},
        product=product.id,
    )

    payment_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            }
        ]
    )

    return payment_link.url




