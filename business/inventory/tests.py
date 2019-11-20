from utils.tests import create_test_supplier, \
    create_test_inventory_product, unauthorised_message, unsuccessful_message, TestAuthenticatedUser, \
    TestStaffSuperUser, \
    TestSupplierMixin, TestInventoryProductMixin


# supplier tests
class TestUnauthorisedCreateSupplier(TestSupplierMixin, TestAuthenticatedUser):

    def setUp(self):
        super().setUp()

    def test_create_supplier(self):
        response = self.create_supplier()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestUnauthorisedRetrieveSupplier(TestSupplierMixin, TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        create_test_supplier()

    def test_retrieve_supplier(self):
        response = self.retrieve_supplier()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_update_supplier(self):
        response = self.update_supplier()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_delete_supplier(self):
        response = self.delete_supplier()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_list_suppliers(self):
        response = self.list_supplier()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedCreateSupplier(TestSupplierMixin, TestStaffSuperUser):

    def setUp(self):
        super().setUp()

    def test_create_supplier(self):
        response = self.create_supplier()
        self.assertEqual(
            response.status_code,
            201,
            unsuccessful_message(response, "Create Supplier", 201))


class TestAuthorisedRetrieveSupplier(TestSupplierMixin, TestStaffSuperUser):
    def setUp(self):
        super().setUp()
        create_test_supplier()

    def test_retrieve_supplier(self):
        """
        Test the retrieval of  product data  an inventory object
        :return: None
        """
        response = self.retrieve_supplier()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "Retrieve Supplier", 200))

    def test_update_supplier(self):
        response = self.update_supplier()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "Update Supplier", 200))

    def test_delete_supplier(self):
        response = self.delete_supplier()
        self.assertEqual(response.status_code, 204, unsuccessful_message(response, "Delete Supplier", 204))

    def test_list_suppliers(self):
        response = self.list_supplier()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "List Supplier", 200))


# product tests
class TestUnauthorisedCreateProduct(TestInventoryProductMixin, TestAuthenticatedUser):

    def setUp(self):
        super().setUp()
        create_test_supplier()

    def test_create_product(self):
        response = self.create_product()
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestUnauthorisedRetrieveProduct(TestInventoryProductMixin, TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        create_test_inventory_product()

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


class TestAuthorisedCreateProduct(TestInventoryProductMixin, TestStaffSuperUser):

    def setUp(self):
        super().setUp()
        create_test_supplier()

    def test_create_product(self):
        response = self.create_product()
        self.assertEqual(response.status_code, 201, unsuccessful_message(response, "Create Product", 201))


class TestRetrieveProduct(TestInventoryProductMixin, TestStaffSuperUser):
    def setUp(self):
        super().setUp()
        create_test_inventory_product()

    def test_retrieve_product(self):
        response = self.retrieve_product()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "Retrieve Product", 200))

    def test_update_product(self):
        response = self.update_product()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "Update Product", 200))

    def test_delete_product(self):
        response = self.delete_product()
        self.assertEqual(response.status_code, 204, unsuccessful_message(response, "Delete Product", 204))

    def test_list_products(self):
        response = self.list_product()
        self.assertEqual(response.status_code, 200, unsuccessful_message(response, "List Products", 200))
