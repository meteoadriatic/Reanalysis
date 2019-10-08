# -*- coding: utf-8 -*-

"""Database module"""
from sqlalchemy.orm import class_mapper, ColumnProperty

from .extensions import db

Column = db.Column
relationship = db.relationship
index = db.Index


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class ExtendedModel(Model):
    """Base model class that includes CRUD convenience methods and some common methods"""

    __abstract__ = True

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [prop.key for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @classmethod
    def get_filtered_data(cls, filters):
        """Return filtered data from the database"""
        return cls.query.filter_by(**filters)

    @classmethod
    def get_all(cls):
        """Return all data from the database"""
        return cls.query.all()
