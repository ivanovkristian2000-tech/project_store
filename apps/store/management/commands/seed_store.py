import random

from datetime import timedelta

from django.core.management.base import BaseCommand

from django.db import transaction

from django.utils import timezone

from faker import Faker



from apps.store.models import (CategoryModel, AddressModel, ProductModel, OrderModel,

                               CustomerModel,  OrderItemModel, ProductDetailModel)



faker = Faker('ru_RU')

class Command(BaseCommand):

    help = 'Заполняет базу тестовыми данными'



    def add_arguments(self, parser):

        parser.add_argument('--clear', action='store_true'

                            , help='Удалить старые данные перед заполнением')



    @transaction.atomic # если что-то упадёт, в базу не запишется ничего

    def handle(self, *args, **options):
        """Заполнить таблицы магазина согласованными случайными данными."""
        from decimal import Decimal
        from uuid import uuid4

        from django.db.models import Max

        from apps.store.models import SupplierModel

        if options.get('clear', False):
            self.clear()

        def create_validated(model, **fields):
            # save() не вызывает full_clean(): проверяем поля до записи в БД.
            instance = model(**fields)
            instance.full_clean()
            instance.save()
            return instance

        def unique_phone(model):
            # Проверяем также существующие записи при запуске без --clear.
            while True:
                phone = '+7' + ''.join(str(random.randrange(10)) for _ in range(10))
                if not model.objects.filter(phone_number=phone).exists():
                    return phone

        categories = []
        categories_created = 0
        max_position = CategoryModel.objects.aggregate(value=Max('position'))['value']
        next_position = 0 if max_position is None else max_position + 1
        for name in ('Бакалея', 'Напитки', 'Сладости', 'Консервы', 'Специи'):
            category = CategoryModel.objects.filter(name=name).first()
            if category is None:
                # position уникален независимо от названия категории.
                category = create_validated(
                    CategoryModel, name=name, position=next_position,
                )
                next_position += 1
                categories_created += 1
            categories.append(category)

        suppliers = []
        for _ in range(5):
            token = uuid4().hex
            suppliers.append(create_validated(
                SupplierModel,
                name=f'{faker.company()[:65]} {token}',
                email=f'supplier-{token}@example.com',
                phone_number=unique_phone(SupplierModel),
            ))

        products = []
        today = timezone.localdate() if timezone.is_aware(timezone.now()) else timezone.now().date()
        for number in range(1, 31):
            category = random.choice(categories)
            quantity = random.randint(0, 200)
            product = create_validated(
                ProductModel,
                name=f'{category.name}: {faker.word()} №{number}',
                category=category,
                supplier=random.choice(suppliers),
                # Цены и вес формируем через Decimal без погрешностей float.
                price=Decimal(random.randint(100, 100000)) / Decimal('100'),
                quantity=quantity,
                article=f'SEED-{uuid4().hex}',
                available=quantity > 0,
            )
            manufactured = today - timedelta(days=random.randint(1, 180))
            create_validated(
                ProductDetailModel,
                product=product,
                description=faker.paragraph(nb_sentences=3),
                manufacturing_date=manufactured,
                expiration_date=today + timedelta(days=random.randint(30, 365)),
                weight=Decimal(random.randint(1, 2500)) / Decimal('100'),
            )
            products.append(product)

        customers = []
        for _ in range(20):
            address = create_validated(
                AddressModel,
                country='Россия',
                city=faker.city()[:100],
                street=faker.street_name()[:255],
                house=faker.building_number()[:6],
            )
            customers.append(create_validated(
                CustomerModel,
                first_name=faker.first_name()[:50],
                last_name=faker.last_name()[:50],
                email=f'customer-{uuid4().hex}@example.com',
                phone_number=unique_phone(CustomerModel),
                address=address,
            ))

        item_count = 0
        for _ in range(40):
            order = create_validated(OrderModel, customer=random.choice(customers))
            # В одном заказе каждый товар встречается только одной строкой.
            for product in random.sample(products, k=random.randint(1, 5)):
                create_validated(
                    OrderItemModel,
                    order=order,
                    product=product,
                    quantity=random.randint(1, 5),
                    # Цена позиции фиксируется на момент создания заказа.
                    price=product.price,
                )
                item_count += 1

        message = (
            f'Создано категорий: {categories_created}, поставщиков: {len(suppliers)}, '
            f'товаров и описаний: {len(products)}, покупателей и адресов: {len(customers)}, '
            f'заказов: 40, позиций заказов: {item_count}.'
        )
        # При ошибке внешняя транзакция откатит и очистку, и новые записи.
        transaction.on_commit(lambda: self.stdout.write(self.style.SUCCESS(message)))

    @transaction.atomic
    def clear(self):
        """Удалить все данные магазина, включая созданные вручную записи."""
        from apps.store.models import SupplierModel

        # Сначала снимаем защищённые связи: позиции -> товары, заказы -> покупатели.
        # Позиции заказов удаляются каскадно вместе с заказами.
        OrderModel.objects.all().delete()
        # Описания товаров также удаляются каскадно (OneToOne с CASCADE).
        ProductModel.objects.all().delete()
        CustomerModel.objects.all().delete()
        AddressModel.objects.all().delete()
        SupplierModel.objects.all().delete()
        CategoryModel.objects.all().delete()
