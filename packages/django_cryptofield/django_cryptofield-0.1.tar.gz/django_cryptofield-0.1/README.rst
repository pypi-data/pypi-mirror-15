Crypto-fields for Django
========================

This package provides database backed, encrypted fields for Django. The fields use database internal mechanisms to encrypt and verify strings completely inside the database. This functionality is interesting for use with passwords that are stored in a database as it allows the database to manage salting, hashing, and verification of the passwords.

Support notes
~~~~~~~~~~~~~

Currently only PostgreSQL is supported as a database backend. I would be happy if someone with experience in MySQL or other databases that support encryption would provide hints or implementations for their favourite database.

Usage
-----

Using ``cryptofield`` is easy::

  from django.db import models
  import cryptofield

  class ModelWithCrypto(models.Model):
      password = cryptofield.CryptoField()

Keyword arguments
~~~~~~~~~~~~~~~~~

The ``CryptoField`` class supports the following keyword arguments:

=========  ============================  ============================
Keyword    Description                   Values
---------  ----------------------------  ----------------------------
algorithm  The hashing algorithm to use  bf (default), md5, xdes, des
=========  ============================  ============================

Requirements (PostgreSQL)
-------------------------

To use this package with PostgreSQL, make sure that the database in use has the ``pgcrypto`` extension activated. To do so, issue the following command to the desired database::

  CREATE EXTENSION IF NOT EXISTS pgcrypto;

If no error occurs, the ``CryptoField`` class can now be used with the database.

