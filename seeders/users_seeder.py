from faker import Faker
from sqlmodel import Session
from app.internal.database.models import User
from app.database import init_db

fake = Faker()


def generate_fake_user():
    return User(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.unique.email(),
    )


def seed_users(count: int = 10000):
    engine = init_db()
    batch_size = 500
    with Session(engine) as session:
        for _ in range(0, count, batch_size):
            batch = [generate_fake_user() for _ in range(min(batch_size, count))]
            session.add_all(batch)
            session.commit()
            count -= batch_size
            print(f"Added {batch_size} users...")


if __name__ == "__main__":
    seed_users(10000)
