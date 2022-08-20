import csv
from pathlib import Path

from faker import Faker
from faker.providers import DynamicProvider

fake = Faker('ru_RU')


def add_news_providers() -> None:
    news_provider = DynamicProvider(
        provider_name="news_provider",
        elements=[
            "Медуза",
            "Лента",
            "Новая газета",
            "АиФ",
            "Лайф",
            "The Insider",
            "Belling Cat",
            "Российская Газета",
            "Комсомольская правда",
            "Литературная газета",
            "Прочтение"
        ]
    )
    fake.add_provider(news_provider)


add_news_providers()


def generate_data(filepath: Path, num_rows=100):
    with open(filepath, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for _ in range(num_rows):
            writer.writerow(_get_fake_row())


def _get_fake_row():
    return [
        fake.unique.sentence(),
        fake.name(),
        fake.uri(),
        fake.news_provider(),
        fake.date_of_birth(maximum_age=1)
    ]

def get_fake_row_dict():
    headers = ["title", "author", "url", "source_name", "published"]
    fake_row = _get_fake_row()
    try:
        return dict(zip(headers, fake_row))
    except:
        print(f"We were not able to convert a fake row into a zip:"
              f"len headers {len(headers)}, len fake row {len(fake_row)}")


if __name__ == '__main__':
    datadir = Path('.data') / 'fake'
    datadir.mkdir(parents=True, exist_ok=True)
    filepath = datadir / 'fakenews.csv'
    generate_data(filepath)
