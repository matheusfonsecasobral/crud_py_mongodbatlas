from config_db import DbConnection
import pandas as pd
from tabulate import tabulate


# noinspection PyStringFormat
class Product:
    def __init__(self, name='', qty='', purchase_price=0, sale_price=0):
        self.name = name
        self.qty = qty
        self.purchase_price = purchase_price
        self.sale_price = sale_price

    @staticmethod
    def see_products():
        df = pd.DataFrame(DbConnection.products.aggregate([{
            "$project": {
                "_id": 0,
                "Name": "$name",
                "Quantity in Stock": "$qty",
                "Purchase Price": "$purchase_price",
                "Sale Price": "$sale_price",
            }
        }]))

        if len(df) == 0:
            print('!INFORMATION! : No products registered yet. Select option 2 to register your first product.')
            return df

        print(tabulate(df, showindex=True, headers=df.columns))
        print('-' * 63)
        return df

    @staticmethod
    def see_products_original_table():
        df = pd.DataFrame(DbConnection.products.find())

        if len(df) == 0:
            print('!INFORMATION! : No products registered yet. Select option 2 to register your first product.')
            return

        return df

    @staticmethod
    def add_product():
        while True:
            try:
                print('!INFORMATION! : Inserting new product! Insert -1 to cancel.')
                item = Product()

                item.name = str(input('Name of product: ')).strip()
                if item.name == '-1':
                    break

                item.qty = int(input('Quantity in stock: '))
                if item.qty == -1:
                    break

                item.purchase_price = float(input('Purchase Price: '))
                if item.purchase_price == -1:
                    break

                item.sale_price = float(input('Sale Price: '))
                if item.sale_price == -1:
                    break

                response = DbConnection.products.insert_one(item.__dict__)

                if response.acknowledged:
                    print('!INFORMATION! : Product registered successfully!')
                    break
                else:
                    print('!INFORMATION! : An error occurred, please try again.')

            except FloatingPointError:
                print('!INFORMATION! : This field need to be a number, please try again.')
            except ValueError:
                print('!INFORMATION! : This field need to be a number, please try again.')
            except:
                print('!INFORMATION! : An error occurred, please try again.')

    @staticmethod
    def update_product(id_field, value_field, obj_id):
        return DbConnection.products.update_one(obj_id, {
            '$set': {
                id_field: value_field
            }
        })

    @staticmethod
    def see_products_to_update():
        df = Product().see_products()
        if len(df) == 0:
            return

        df = Product().see_products_original_table()
        obj_id = int(input('!INFORMATION! - Insert id of product you want update. Insert -1 to return:'))

        if obj_id == -1:
            return

        while True:
            try:
                obj_dict = df.to_dict(orient='records')[obj_id]
                id_field = int(
                    input('!INFORMATION! - Updating Product ID {}, what you want update? Insert -1 to return:\n'
                          '[1] Name\n'
                          '[2] Quantity in Stock\n'
                          '[3] Purchase Price\n'
                          '[4] Sale Price\n'
                          'Response:'.format(obj_id)))

                if id_field == -1:
                    break

                value_field = -1

                if id_field == 1:
                    id_field = 'name'
                    value_field = str(
                        input('!INFORMATION! - Updating Product ID {}, updating {}. Insert -1 to return:\n'
                              'Response:'.format(obj_id, "'Name'")))
                elif id_field == 2:
                    id_field = 'qty'
                    value_field = \
                        int(
                            input('!INFORMATION! - Updating Product ID {}, updating {}. Insert -1 to return:\n'
                                  'Response:'.format(obj_id, "'Quantity in Stock'")))
                elif id_field == 3:
                    id_field = 'purchase_price'
                    value_field = \
                        float(
                            input('!INFORMATION! - Updating Product ID {}, updating {}. Insert -1 to return:\n'
                                  'Response:'.format(obj_id, "'Purchase Price'")))
                elif id_field == 4:
                    id_field = 'sale_price'
                    value_field = \
                        float(
                            input('!INFORMATION! - Updating Product ID {}, updating {}. Insert -1 to return:\n'
                                  'Response:'.format(obj_id, "'Sale Price'")))

                if value_field == -1:
                    break

                response = Product.update_product(id_field, value_field, {k: obj_dict[k] for k in list(obj_dict)[:1]})

                if response.acknowledged:
                    print('!INFORMATION! : Product updated successfully!')
                    break
                else:
                    print('!INFORMATION! : An error occurred, please try again.')


            except ValueError:
                print('!INFORMATION! : This field need to be a number, please try again.')
            except:
                print('!INFORMATION! : An error occurred, please try again.')

    @staticmethod
    def delete_product(df):
        while True:
            try:
                obj_id = int(
                    input('!INFORMATION! - Please, insert the id of product you want delete. Insert -1 to return:'))

                if obj_id == -1:
                    break

                obj_dict = df.to_dict(orient='records')[obj_id]
                response = DbConnection.products.delete_one({k: obj_dict[k] for k in list(obj_dict)[:1]})

                if response.acknowledged:
                    print('!INFORMATION! : Product deleted successfully!')
                    break
                else:
                    print('!INFORMATION! : An error occurred, please try again.')

            except IndexError:
                print('!INFORMATION! : The entered id does not exist, please try again.')
            except ValueError:
                print('!INFORMATION! : Id need to be a number, please try again.')
            except:
                print('!INFORMATION! : An error occurred, please try again.')

    @staticmethod
    def see_products_to_delete():
        df = Product().see_products()
        if len(df) == 0:
            return

        df = Product().see_products_original_table()
        Product.delete_product(df)



