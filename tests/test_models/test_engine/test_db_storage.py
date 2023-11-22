#!/usr/bin/python3
"""Defines unittests for models/engine/db_storage.py.

Unittest classes:
    TestClass_instantiation
    TestDBStorage_methods
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestClass_instantiation(unittest.TestCase):
    """Testing class instantiation"""

    def test_no_args(self):
        self.assertEqual(type(DBStorage()), DBStorage)

    def test_args(self):
        with self.assertRaises(TypeError):
            DBStorage(None)

    def test_models_storage(self):
        self.assertEqual(type(models.storage), DBStorage)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestMethods(unittest.TestCase):
    """testing methods of the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_all_return_type(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_method_without_args(self):
        from models import storage

        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        dict_objs = storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

    def test_all_method_with_args(self):
        from models import storage

        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        # All states
        states_objs = storage.all(State)

        self.assertIn(tafilalet, states_objs.values())
        self.assertNotIn(errachidia, states_objs.values())
        self.assertNotIn(arfoud, states_objs.values())

        # All cities
        cities_objs = storage.all(City)

        self.assertNotIn(tafilalet, cities_objs.values())
        self.assertIn(errachidia, cities_objs.values())
        self.assertIn(arfoud, cities_objs.values())

    def test_new_method(self):
        base_m = BaseModel()
        models.storage.new(base_m)
        self.assertIn("BaseModel." + base_m.id, models.storage.all().keys())
        self.assertIn(base_m, models.storage.all().values())

    def test_new_method_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), "testing")

    def test_save_method(self):
        base_m = BaseModel()
        models.storage.new(base_m)
        models.storage.save()
        with open("file.json", "r") as f:
            storage_content = f.read()
            self.assertIn("BaseModel." + base_m.id, storage_content)

    def test_save_method_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload_method(self):
        base_m = BaseModel()

        models.storage.new(base_m)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn("BaseModel." + base_m.id, storage_objs)

    def test_reload_method_args(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

    def test_delete(self):
        from models import storage

        tafilalet = State(name="Tafilalet")
        errachidia = City(name="Errachidia", state_id=tafilalet.id)
        arfoud = City(name="Arfoud", state_id=tafilalet.id)

        tafilalet.save()
        errachidia.save()
        arfoud.save()

        dict_objs = storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

        storage.delete(errachidia)

        dict_objs = storage.all()

        self.assertIn(tafilalet, dict_objs.values())
        self.assertNotIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())

        storage.delete(tafilalet)

        dict_objs = storage.all()

        self.assertNotIn(tafilalet, dict_objs.values())
        self.assertNotIn(errachidia, dict_objs.values())
        self.assertIn(arfoud, dict_objs.values())


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithUser(unittest.TestCase):
    """testing that DBStorage class correctly handles User class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = User()
        models.storage.new(obj)
        self.assertIn("User." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = User()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("User." + obj.id, storage_content)

    def test_reload_method(self):
        obj = User()
        key = "User." + obj.id
        obj.name = 'Link'

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'Link')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithState(unittest.TestCase):
    """testing that DBStorage class correctly handles State class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = State()
        models.storage.new(obj)
        self.assertIn("State." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = State()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("State." + obj.id, storage_content)

    def test_reload_method(self):
        obj = State()
        key = "State." + obj.id
        obj.name = 'California'

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'California')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithCity(unittest.TestCase):
    """testing that DBStorage class correctly handles City class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = City()
        models.storage.new(obj)
        self.assertIn("City." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = City()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("City." + obj.id, storage_content)

    def test_reload_method(self):
        obj = City()
        key = "City." + obj.id
        obj.name = 'Tokyo'

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'Tokyo')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithPlace(unittest.TestCase):
    """testing that DBStorage class correctly handles Place class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = Place()
        models.storage.new(obj)
        self.assertIn("Place." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = Place()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("Place." + obj.id, storage_content)

    def test_reload_method(self):
        obj = Place()
        key = "Place." + obj.id
        obj.name = 'Square Park'
        obj.max_guest = 5
        obj.latitude = 77.8
        obj.longitude = 45.23
        bathroom, kitchen, balcony = Amenity(), Amenity(), Amenity()
        list_amenity_ids = [bathroom.id, kitchen.id, balcony.id]
        obj.amenity_ids = list_amenity_ids

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)

        self.assertEqual(type(storage_objs[key].id), str)
        self.assertEqual(storage_objs[key].id, obj.id)

        self.assertEqual(type(storage_objs[key].name), str)
        self.assertEqual(storage_objs[key].name, 'Square Park')

        self.assertEqual(type(storage_objs[key].max_guest), int)
        self.assertEqual(storage_objs[key].max_guest, 5)

        self.assertEqual(type(storage_objs[key].latitude), float)
        self.assertEqual(storage_objs[key].latitude, 77.8)

        self.assertEqual(type(storage_objs[key].longitude), float)
        self.assertEqual(storage_objs[key].longitude, 45.23)

        self.assertEqual(type(storage_objs[key].amenity_ids), list)
        self.assertEqual(storage_objs[key].amenity_ids, list_amenity_ids)


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithAmenity(unittest.TestCase):
    """testing that DBStorage class correctly handles Amenity class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = Amenity()
        models.storage.new(obj)
        self.assertIn("Amenity." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = Amenity()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("Amenity." + obj.id, storage_content)

    def test_reload_method(self):
        obj = Amenity()
        key = "Amenity." + obj.id
        obj.name = 'Kitchen'

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].name, 'Kitchen')


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Using FileStorage')
class TestWithReview(unittest.TestCase):
    """testing that DBStorage class correctly handles Review class"""

    @classmethod
    def setUpClass(cls):
        try:
            shutil.copy2("file.json", "temp")
            DBStorage._DBStorage__engine = "temp"
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("temp")
            DBStorage._DBStorage__engine = "file.json"
        except IOError:
            pass
        DBStorage._DBStorage__objects = {}

    def test_new_method(self):
        obj = Review()
        models.storage.new(obj)
        self.assertIn("Review." + obj.id, models.storage.all().keys())
        self.assertIn(obj, models.storage.all().values())

    def test_save_method(self):
        obj = Review()
        models.storage.new(obj)
        models.storage.save()
        with open("temp", "r") as f:
            storage_content = f.read()
            self.assertIn("Review." + obj.id, storage_content)

    def test_reload_method(self):
        obj = Review()
        key = "Review." + obj.id
        obj.text = 'Excellent'

        models.storage.new(obj)
        models.storage.save()
        models.storage.reload()
        storage_objs = DBStorage._DBStorage__objects

        self.assertIn(key, storage_objs)
        self.assertEqual(storage_objs[key].id, obj.id)
        self.assertEqual(storage_objs[key].text, 'Excellent')


if __name__ == "__main__":
    unittest.main()
