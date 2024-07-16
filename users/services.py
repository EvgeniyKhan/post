import stripe

from config.settings import STRIPE_API_KEY, STRIPE_SUCCESS_URL


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
        success_url=STRIPE_SUCCESS_URL,
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def check_payment_status(payment_intent_id):
    try:
        payment_intent = stripe.checkout.Session.retrieve(payment_intent_id)
        return payment_intent["payment_status"] == 'paid'
    except stripe.error.StripeError as e:
        # Обработка ошибок Stripe
        return False
