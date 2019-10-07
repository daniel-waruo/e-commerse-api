from rest_framework.reverse import reverse

from utils.tests import UserTestCase, test_category_params, create_test_category, \
    create_test_cms_product, create_test_inventory_product


class TestCreateCategory(UserTestCase):

    def setUp(self):
        super().setUp()

    def test_create_category(self):
        """
        Test whether the api can make a category
        :return:
        """
        self.client.login(username="test", password="test")
        url = reverse("cms:add_category")
        response = self.client.post(url, test_category_params)
        self.assertEqual(response.status_code, 201,
                         'Category not Created.Expected Response Code 201, received {0} instead.'
                         'It returned {1}'
                         .format(response.status_code, response.content))


class TestCategoryView(UserTestCase):
    def setUp(self):
        super().setUp()
        create_test_category()

    def test_retrieve_category(self):
        """
        Test the retrieval of  product data  an cms category
        :return: None
        """
        self.client.login(username="test", password="test")
        url = reverse('cms:category_view', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Retrieve Category is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_category(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:category_view', kwargs={'pk': 1})
        response = self.client.put(url, data={
            "name": "Test Category Update",
            "slug": "test-category-update",
            "parent": ''
        })
        self.assertEqual(response.status_code, 200,
                         'Retrieve Category is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_delete_category(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:category_view', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204,
                         'Delete Category is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_list_categories(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:list_categories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Listing of Categories is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))


class TestCreateProduct(UserTestCase):

    def setUp(self):
        super().setUp()
        create_test_category()
        create_test_inventory_product()

    def test_create_product(self):
        """
        Test whether the api can make a category
        :return:
        """
        self.client.login(username="test", password="test")
        url = reverse("cms:add_product")

        response = self.client.post(url, {
            "product": 1,
            "name": "Test Cms Product",
            # "images": ["https://ucarecdn.com/0799e306-6da7-4c94-bc54-29cf96957f25/-/resize/50x50/"],
            "category": 1,
            "price": 2000.87,
            "price_currency": "USD",
            "discount_price": 1800.87,
            "discount_price_currency": "USD",
            "slug": "cms-product",
            "description": "This is the Product Used to test our Cms Product"
        })
        self.assertEqual(response.status_code, 201,
                         'CMS Product not Created.Expected Response Code 201, received {0} instead.'
                         'It returned {1}'
                         .format(response.status_code, response.content))


class TestProductView(UserTestCase):
    def setUp(self):
        super().setUp()
        create_test_cms_product()

    def test_retrieve_product(self):
        """
        Test the retrieval of  product data  an cms category
        :return: None
        """
        self.client.login(username="test", password="test")
        url = reverse('cms:product_view', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Retrieve CMS PRODUCT is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_product(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:product_view', kwargs={'pk': 1})
        response = self.client.put(url, data={
            "product": 1,
            "name": "Test Cms Product Update",
            "images": ["", "", ""],
            "category": 1,
            "price": 2000.87,
            "discount_price": 1800.87,
            "slug": "cms-product-update",
            "description": "This is the Product Used to test our Cms Product"
        })
        self.assertEqual(response.status_code, 200,
                         'Update Product is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_delete_product(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:product_view', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204,
                         'Delete CMS Product is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_list_products(self):
        self.client.login(username="test", password="test")
        url = reverse('cms:list_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Listing of CMS Products is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
