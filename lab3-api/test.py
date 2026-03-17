from db.database import engine, Session
from models.models import Base, User, Currency, Subscription

Base.metadata.create_all(engine)

with Session() as session:
    user1 = User(username="test_user", email="test@mail.ru")
    user2 = User(username="test_user2", email="test2@mail.ru")

    currency1 = Currency(code="USD", name="US Dollar")
    currency2 = Currency(code="EUR", name="Euro")

    session.add(currency1)
    session.add(currency2)
    session.add(user1)
    session.add(user2)

    session.commit()

    subscription1 = Subscription(user_id=user1.id, currency_id=currency1.id)
    subscription2 = Subscription(user_id=user1.id, currency_id=currency2.id)
    subscription3 = Subscription(user_id=user2.id, currency_id=currency1.id)

    session.add(subscription1)
    session.add(subscription2)
    session.add(subscription3)

    session.commit()

    print(user1.subscriptions)
    print(currency1.subscriptions)
