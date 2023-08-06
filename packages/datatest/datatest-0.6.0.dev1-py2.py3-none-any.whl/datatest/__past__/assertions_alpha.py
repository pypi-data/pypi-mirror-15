# -*- coding: utf-8 -*-
"""Backwards compatibility for assertion methods from alpha version."""
from __future__ import absolute_import
from datatest import DataTestCase


DataTestCase.assertColumnSet = DataTestCase.assertDataColumns
DataTestCase.assertValueSet = DataTestCase.assertDataSet
DataTestCase.assertValueSum = DataTestCase.assertDataSum
DataTestCase.assertValueCount = DataTestCase.assertDataCount
DataTestCase.assertValueRegex = DataTestCase.assertDataRegex
DataTestCase.assertValueNotRegex = DataTestCase.assertDataNotRegex


def _assertColumnSubset(self, ref=None, msg=None):
    """Test that the set of subject columns is a subset of reference
    columns.  If *ref* is provided, it is used in-place of the set
    from ``referenceData``.
    """
    with self.allowMissing():
        self.assertColumnSet(ref, msg)
DataTestCase.assertColumnSubset = _assertColumnSubset


def _assertColumnSuperset(self, ref=None, msg=None):
    """Test that the set of subject columns is a superset of reference
    columns.  If *ref* is provided, it is used in-place of the set
    from ``referenceData``.
    """
    with self.allowExtra():
        self.assertColumnSet(ref, msg)
DataTestCase.assertColumnSuperset = _assertColumnSuperset


def _assertValueSubset(self, column, ref=None, msg=None, **filter_by):
    """Test that the set of subject values is a subset of reference
    values for the given *column*.  If *ref* is provided, it is used
    in place of the set from ``referenceData``.
    """
    with self.allowMissing():
        self.assertValueSet(column, ref, msg, **filter_by)
DataTestCase.assertValueSubset = _assertValueSubset


def _assertValueSuperset(self, column, ref=None, msg=None, **filter_by):
    """Test that the set of subject values is a superset of reference
    values for the given *column*.  If *ref* is provided, it is used
    in place of the set from ``referenceData``.
    """
    with self.allowExtra():
        self.assertValueSet(column, ref, msg, **filter_by)
DataTestCase.assertValueSuperset = _assertValueSuperset
