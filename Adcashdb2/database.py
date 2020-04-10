from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# postgresql+psycopg2://postgres:root@localhost/catalogofproducts
# postgresql+psycopg2://user:password@localhost/databaseName
engine = create_engine('''postgresql+psycopg2://postgres:Transcriber123@localhost/adcashdb''')
db = scoped_session(sessionmaker(bind=engine))


def get_list_of_categories():
    query = "SELECT * FROM category_table;"
    result = db.execute(query).fetchall()  # [(1,meat),(2,fruit)] data returned in this form
    db.commit
    # JSON FROMAT
    # {
    #   KEY: VALUE
    # }
    json_object = {
        'format': {'CATEGORY ID': 'CATEGORY NAME'},
        'data': {}
    }
    for categoryID, categoryName in result:  # [(1,meat),(2,fruit)]
        json_object['data'][categoryID] = categoryName
    return json_object


def get_list_of_products_from_concrete_category(category: str):
    query = f'''SELECT * 
FROM public.product_table
WHERE id_category=(SELECT category_id from public.category_table WHERE category_name='{category}');'''
    result = db.execute(query).fetchall()
    db.commit
    json_object = {
        'format': {'CATEGORY ID': 'CATEGORY NAME'},
        'data': {}
    }
    for productID, productName, productCategory in result:
        json_object['data'][productID] = productName
    return json_object


def create_category(category_name: str):
    db.execute(f'''INSERT INTO public.category_table(
	category_id, category_name)
	VALUES (nextval('auto_increment'), '{category_name}');''')
    db.commit()


def update_category(old_category: str, new_category: str):
    query = f'''UPDATE public.category_table
	SET category_name='{new_category}'
	WHERE category_name='{old_category}';'''
    db.execute(query)
    db.commit()


def delete_category(category: str, methods=['GET']):
    query = f'''DELETE FROM public.category_table
	WHERE category_name='{category}';'''
    db.execute(query)
    db.commit()


def create_product(product_name: str, product_category):
    db.execute(f'''INSERT INTO public.product_table(
	product_id, product_name, id_category)
	VALUES (nextval('auto_increment'), '{product_name}', (SELECT category_id FROM public.category_table WHERE category_name='{product_category}'));
	''')
    db.commit()


def update_product(old_product: str, new_product: str, new_category: str):
    query = f'''UPDATE public.product_table
	SET product_name='{new_product}', id_category=(SELECT category_id FROM public.category_table WHERE category_name='{new_category}')
	WHERE product_name='{old_product}';'''
    db.execute(query)
    db.commit()


def delete_product(name_product: str):
    query = f'''DELETE FROM public.product_table
	WHERE product_name='{name_product}';'''
    db.execute(query)
    db.commit()


def main():
    print(get_list_of_categories())


if __name__ == '__main__':
    main()
