# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_DB import Catalog, Base, Items, User, ItemPhotos

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Users Data
admin_user = User(name="Admin", email='admin@admin.com', photo='https://www.knowmuhammad.org/img/noavatarn.png')
session.add(admin_user)
session.commit()

#    Catalogs    #
# First Catalog
catalog1 = Catalog(name='Match Kits', photo='')
session.add(catalog1)
session.commit()

# First Catalog Items
item1_1 = Items(name='JUVENTUS HOME AUTHENTIC JERSEY 2018/19',
                description=("The \"Authentic\" jersey is the version worn by our team on the pitch. The fit, "
                             "much tighter than the Home Replica version, is designed for the athlete's body. New "
                             "fabric Technology guarantees better breathability, helping to enhance performance. A "
                             "premium heat transfer crest keeps this jersey as light as possible."),
                price= '400', catalog=catalog1, user=admin_user)
session.add(item1_1)
session.commit()

# adding item1_1 list of photos
item1_1_photo1 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26367/product.jpg',
                             items=item1_1, catalog=catalog1)
session.add(item1_1_photo1)
session.commit()

item1_1_photo2 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/29275/product.jpg',
                             items=item1_1, catalog=catalog1)
session.add(item1_1_photo2)
session.commit()

item1_1_photo3 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26369/product.jpg',
                             items=item1_1, catalog=catalog1)
session.add(item1_1_photo3)
session.commit()


# Second Catalog Items
item2_1 = Items(name='JUVENTUS HOME SHORTS 2018/19',
                description=("The Home shorts 2018/19 complete the kit that our champions will wear in the home "
                            "challenges. A simple and innovative design that enhances the contemporary look without "
                            "forgetting the legendary kits of the past."),
                price='450', catalog=catalog1, user=admin_user)
session.add(item2_1)
session.commit()


# adding item2_1 list of photos
item2_1_photo1 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26273/product.jpg',
                             items=item2_1, catalog=catalog1)
session.add(item2_1_photo1)
session.commit()

item2_1_photo2 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26275/product.jpg',
                             items=item2_1, catalog=catalog1)
session.add(item2_1_photo2)
session.commit()

item2_1_photo3 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26277/product.jpg',
                             items=item2_1, catalog=catalog1)
session.add(item2_1_photo3)
session.commit()


# Third Catalog Items
item3_1 = Items(name='JUVENTUS GOALKEEPER JERSEY 2018/19',
                description=("THE GOALKEEPER'S HOME SHIRT 2018/2019 WILL HAVE THE TASK OF DEFENDING THE BIANCONERA "
                            "GOAL IN THE CHALLENGES THAT AWAIT US."),
                price='600', catalog=catalog1, user=admin_user)
session.add(item3_1)
session.commit()

# adding item3_1 list of photos
item3_1_photo1 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26747/product.jpg',
                             items=item3_1, catalog=catalog1)
session.add(item3_1_photo1)
session.commit()

item3_1_photo2 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/29291/product.jpg',
                             items=item3_1, catalog=catalog1)
session.add(item3_1_photo2)
session.commit()

item3_1_photo3 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/27873/product.jpg',
                             items=item3_1, catalog=catalog1)
session.add(item3_1_photo3)
session.commit()

item4_1 = Items(name='JUVENTUS CLAY Z.N.E. JACKET KNIT 2018/19',
                description=("THE Z.N.E. SWEATSHIRT 2018/19 IS THE ACCESSORY THAT COMPLETES THE HOME KIT. PERFECT "
                            "FOR PREPARING FOR EVERY CHALLENGE IN THE BEST WAY AND FINDING THE RIGHT FOCUS BEFORE "
                            " THE BIG MATCHES."),
                price='400',catalog=catalog1, user=admin_user)
session.add(item4_1)
session.commit()

# adding item4_1 list of photos
item4_1_photo1 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26493/product.jpg',
                             items=item4_1, catalog=catalog1)
session.add(item4_1_photo1)
session.commit()

item4_1_photo2 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26495/product.jpg',
                             items=item4_1, catalog=catalog1)
session.add(item4_1_photo2)
session.commit()

item4_1_photo3 = ItemPhotos(photo_url='https://store.juventus.com/data/store/product/2/26497/product.jpg',
                             items=item4_1, catalog=catalog1)
session.add(item4_1_photo3)
session.commit()


# Second Catalog
catalog2 = Catalog(name='Training', photo='')
session.add(catalog2)
session.commit()

# Second Catalog Items
# item1_2 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog2, user=admin_user)
# session.add(item1_2)
# session.commit()
#
# item2_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item3_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item4_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
#
# Third Catalog
catalog3 = Catalog(name='Apparel', photo='')
session.add(catalog3)
session.commit()

# # Third Catalog Items
# item1_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item2_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item3_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item4_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# Fourth Catalog
catalog4 = Catalog(name='Accessories', photo='')
session.add(catalog4)
session.commit()
#
# # Fourth Catalog Items
# item1_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item2_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item3_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# item4_1 = Items(name='',
#                 description='',
#                 photo="https://store.juventus.com/data/store/product/2/26367/thumbnail.120x120.jpg",
#                 catalog=catalog1, user=admin_user)
# session.add(catalog1)
# session.commit()
#
# Fifth Catalog
catalog5 = Catalog(name='Gift Ideas', photo='')
session.add(catalog5)
session.commit()
print "added catalog items!"