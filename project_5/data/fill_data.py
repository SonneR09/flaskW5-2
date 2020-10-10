import csv
from app import db, Meal, Category


def fill_db():
    with open('delivery_categories.csv', encoding='utf-8') as cat:
        categories = csv.DictReader(cat)
        for category in categories:
            categ = Category(title=category['title'])
            db.session.add(categ)
        db.session.commit()

    with open('delivery_items.csv', encoding='utf-8') as f:
        items = csv.DictReader(f)
        for item in items:
            category = db.session.query(Category).filter(Category.id == int(item['category_id'])).first()
            meal = Meal(title=item['title'], price=int(item['price']), description=item['description'],
                        picture=item['picture'], categories=category)
            db.session.add(meal)

    db.session.commit()


if __name__ == '__main__':
    fill_db()