from flask import Flask, request
from flask import jsonify
import database

app = Flask("__name__")
app.config["DEBUG"] = True


@app.route("/getallcategories")
def getting_categories():
    data = database.get_list_of_categories()
    return jsonify(data)

@app.route("/")
def home():
    return '''
        <h1>Welcome</h1>
    '''


@app.route("/getproductsofcategory/<string:category>")
def getting_products(category):
    data = database.get_list_of_products_from_concrete_category(category)
    return jsonify(data)


@app.route("/createcategory/<string:category>")
def category_create(category):
    data = database.create_category(category)
    return 'category created'


@app.route("/updatecategory/<string:oldcategory>/<string:newcategory>")
def category_update(oldcategory, newcategory):
    data = database.update_category(oldcategory, newcategory)
    return 'category updated'


@app.route("/deletecategory/<string:category>")
def category_delete(category):
    data = database.delete_category(category)
    return 'category deleted'


@app.route("/createproduct/<string:product>/<string:category>")
def product_create(product, category):
    data = database.create_product(product, category)
    return 'product created'


@app.route("/updateproduct/<string:oldproduct>/<string:newproduct>/<string:category>")
def product_update(oldproduct, newproduct, category):
    data = database.update_product(oldproduct, newproduct, category)
    return 'product updated'


@app.route("/deleteproduct/<string:product>")
def product_delete(product):
    data = database.delete_product(product)
    return 'product deleted'


if __name__ == "__main__":
    app.run()
