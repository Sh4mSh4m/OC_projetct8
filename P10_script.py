import csv
import requests
import pdb
import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Table, Text, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://hieudb:hieuhieu81@localhost:5432/{}'.format('purbeurre', echo=False))


Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, Sequence('product_id_seq'), primary_key=True)
    url = Column(String(200))
    name = Column(Text)
    description = Column(Text)
    quantity = Column(String(100))
    brands = Column(String(100))
    nutrition_grade = Column(Float, default="NULL")
    main_category = Column(String(100))
    productImageUrl = Column(String(200))
    productImageThumbUrl = Column(String(200))
    __table_args__ = (
        UniqueConstraint('name', 'description', 'quantity'),
    )


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, Sequence('category_id_seq'), primary_key=True)
    name_category = Column(String(100), unique=True)


class ProductCategory(Base):
    __tablename__ = 'products_categories'
    product_id = Column(Integer, ForeignKey('products.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    __table_args__ = (
        PrimaryKeyConstraint('product_id', 'category_id', name='uix_2'),
    )


Base.metadata.create_all(engine)


def productAdd(engine):
    with open("update_product.csv") as f:
        content = csv.reader(f, delimiter=";")
        index = 0
        for line in content:
            Session = sessionmaker(bind=engine)
            session = Session()
            productSpec = {}
            productSpec['url'] = line[0]
            productSpec['name'] = line[1]
            productSpec['description'] = line[2]
            productSpec['quantity'] = line[3]
            productSpec['brands'] = line[4]
            productSpec['nutrition_grade'] = line[9]
            productSpec['main_category'] = line[6]
            productSpec['productImageUrl'] = line[7]
            productSpec['productImageThumbUrl'] = line[8]
            productDbEntry = Product(**productSpec)
            try:
                session.merge(productDbEntry)
                session.commit()
                print("done it")
            except:
                session.rollback()
                print("failed")
            finally:
                index += 1
                print("hey i made it there {}".format(index))
                categoriesAdd(productSpec, session, line)


def categoriesAdd(productSpec, session, line):
    try:
        productId = session.query(Product).filter_by(**productSpec).first().id
        print(productId)
        categoriesList = line[5].split(',')
        for category in categoriesList:
            print(category)
            categoryDbEntry = Category(name_category = category.strip())
            try:
                session.add(categoryDbEntry)
                session.commit()
            except:
                session.rollback()
            finally:
                categoryId = session.query(Category).filter_by(name_category = category.strip()).first().id
                productcategoryDbEntry = ProductCategory(product_id = productId, category_id = categoryId)
                try:
                    session.add(productcategoryDbEntry)
                    session.commit()
                except:
                    session.rollback()
                finally:
                    pass
    except:
        session.rollback()
        pass


def csv_treatment():
    #downloads file from link
    import requests
    response = requests.get('https://cdn03.nintendo-europe.com/media/images/10_share_images/portals_3/H2x1_SuperMario_Hub_image1600w.jpg')
    with open('raw_product.jpg', 'wb') as f:
        f.write(response.content)

    # Removes unused columns from the downloaded CSV file
    f = pd.read_csv("products.csv",sep='\t')
    keep_col = ['url','product_name', 'generic_name', 'quantity', 'brands', 'categories_fr', 'main_category_fr', 'image_url', 'image_small_url', 'nutrition-score-fr_100g']
    new_f = f[keep_col]
    new_f.to_csv("new_product.csv",sep=';', index = False)

    # Compares older csv with the latest csv file:
    with open('new_product.csv', 'r') as t1, open('old_product.csv', 'r') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open('update_product.csv', 'w') as outFile:
        for line in filetwo:
            if line not in fileone:
                outFile.write(line)


def cleanup():
    os.remove("old_product.csv")
    os.rename("new_product.csv", "old_product.csv")
    os.remove("update_product.csv")


def main():
    csv_treatment()
    if os.path.isfile("update_product.csv"):
        productAdd(engine)
    cleanup()

if __name__ == "__main__":
    main()
