from utils.tests import (
    TestAuthenticatedUser,
    create_test_category,
    create_test_cms_product,
    create_test_inventory_product,
    unauthorised_message,
    TestCategoryMixin, TestCmsProductMixin, TestStaffSuperUser, unsuccessful_message)


class TestUnauthorisedCreateCategory(TestCategoryMixin, TestAuthenticatedUser):

    def setUp(self):
        super().setUp()

    def test_create_category(self):
        """
        Test whether the api can make a category
        :return:
        """
        response = self.create_category()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedCreateCategory(TestCategoryMixin, TestStaffSuperUser):

    def setUp(self):
        super().setUp()

    def test_create_category(self):
        """
        Test whether the api can make a category
        :return:
        """
        response = self.create_category()
        self.assertEqual(
            response.status_code,
            201,
            unsuccessful_message(response, "Create Category", 201))


class TestUnauthorisedCategoryView(TestCategoryMixin, TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        create_test_category()

    def test_retrieve_category(self):
        response = self.retrieve_category()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_update_category(self):
        response = self.update_category()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_delete_category(self):
        response = self.delete_category()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_list_categories(self):
        response = self.list_category()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedCategoryView(TestCategoryMixin, TestStaffSuperUser):
    def setUp(self):
        super().setUp()
        create_test_category()

    def test_retrieve_category(self):
        response = self.retrieve_category()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "Retrieve Category", 200)
        )

    def test_update_category(self):
        response = self.update_category()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "Update Category", 200)
        )

    def test_delete_category(self):
        response = self.delete_category()
        self.assertEqual(
            response.status_code,
            204,
            unsuccessful_message(response, "Delete Category", 204)
        )

    def test_list_categories(self):
        response = self.list_category()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "List Categories", 200)
        )


class TestUnauthorisedCreateProduct(TestCmsProductMixin, TestAuthenticatedUser):

    def setUp(self):
        super().setUp()
        create_test_category()
        create_test_inventory_product()

    def test_create_product(self):
        response = self.create_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedCreateProduct(TestCmsProductMixin, TestStaffSuperUser):

    def setUp(self):
        super().setUp()
        create_test_category()
        create_test_inventory_product()

    def test_create_product(self):
        response = self.create_product()
        self.assertEqual(
            response.status_code,
            201,
            unsuccessful_message(response, "Create Product", 201)
        )


class TestUnauthorisedProductView(TestCmsProductMixin, TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        create_test_cms_product()

    def test_retrieve_product(self):
        response = self.retrieve_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_update_product(self):
        response = self.update_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_delete_product(self):
        response = self.delete_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_list_products(self):
        response = self.list_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedProductView(TestCmsProductMixin, TestStaffSuperUser):
    def setUp(self):
        super().setUp()
        create_test_cms_product()

    def test_retrieve_product(self):
        response = self.retrieve_product()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "Retrieve Product", 200)
        )

    def test_update_product(self):
        response = self.update_product()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "Update Product", 200)
        )

    def test_delete_product(self):
        response = self.delete_product()
        self.assertEqual(
            response.status_code,
            204,
            unsuccessful_message(response, "Delete Product", 204)
        )

    def test_list_products(self):
        response = self.list_product()
        self.assertEqual(
            response.status_code,
            200,
            unsuccessful_message(response, "List Categories", 200)
        )
