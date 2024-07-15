import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(pk, data):
    """
    Создает продукт в Stripe.

    Args:
        pk (int): Идентификатор продукта.
        data (str): Данные для описания продукта.

    Returns:
        str: Идентификатор созданного продукта в Stripe.
    """
    description = str(pk) + "дата платежа" + str(data)
    payment = stripe.Product.create(name=f"{pk}", description=description)
    return payment.get("id")


def create_stripe_price():
    """
    Создает цену в Stripe.

    Returns:
        dict: Информация о созданной цене в Stripe.
    """
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=1500 * 100,
        product_data={"name": "Оплата выбранного продукта"},
    )
    return stripe_price


def create_stripe_session(price):
    """
    Создает сессию оплаты в Stripe.

    Args:
        price (dict): Информация о цене в Stripe.

    Returns:
        tuple: Идентификатор и URL созданной сессии оплаты в Stripe.
    """
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_payment_status(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return payment_intent.status == 'succeeded'
    except stripe.error.StripeError as e:
        # Обработка ошибок Stripe
        return False
