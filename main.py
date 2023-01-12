from Entities.Product import Product
from datetime import datetime


class Main:
    if __name__ == '__main__':
        print('Welcome to the Stock System - {}'.format(datetime.today().ctime()))
        while True:
            response = str(input('[1] Check All Products\n'
                                 '[2] Insert New Product\n'
                                 '[3] Update Product\n'
                                 '[4] Delete Product\n'
                                 'Response:')).strip()
            if response in ('1', '2', '3', '4'):
                if response == '1':
                    Product.see_products()
                if response == '2':
                    Product.add_product()
                if response == '3':
                    Product.see_products_to_update()
                if response == '4':
                    Product.see_products_to_delete()
            else:
                print('!INFORMATION! : Incorrect Number, please try another value.')
