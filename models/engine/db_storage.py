#!/usr/bin/python3
'''This module defines a class to manage database storage for hbnb clone'''
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base


class DBStorage:
    '''This class manages database storage of hbnb models in MySQL DB'''
    __engine = None
    __session = None

    def __init__(self):
        '''Create DBStorage engine and drop tables if testing'''
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')

        db_link = f'mysql+mysqldb://{USER}:{PWD}@{HOST}:3306/{DB}'
        self.__engine = create_engine(db_link, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def reload(self):
        '''
        Create all the tables in the database,
        then create the current database session
        '''
        from models.base_model import Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)

        ScopedSession = scoped_session(sessionmaker(bind=self.__engine,
                                                    expire_on_commit=False))
        self.__session = ScopedSession()

    def new(self, obj=None):
        '''Add the object to the current database session'''
        if obj:
            self.__session.add(obj)

    def save(self):
        '''Commit all the changes of the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete a record from the current database session'''

        if obj:
            self.__session.delete(obj)
            self.save()

    def all(self, cls=None):
        '''
        Query on the current database session all objects,
        or a specific class's objects depending of the class name
        '''
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        objs_dict = {}

        engine = self.__engine
        session = self.__session

        tables = [State, City, User, Place, Review, Amenity]

        if cls:
            tables = [cls]
        for t_name in tables:
            objs = session.query(t_name).all()
            for obj in objs:
                _cl = obj.__class__.__name__
                _id = obj.id
                objs_dict[f'{_cl}.{_id}'] = obj

        return objs_dict

    def close(self):
        '''Close the session'''
        self.__session.close()
