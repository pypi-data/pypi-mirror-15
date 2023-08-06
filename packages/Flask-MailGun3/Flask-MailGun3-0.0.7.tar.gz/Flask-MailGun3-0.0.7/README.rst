Flask-MailGun
=============

|Latest Version| |Build Status| |Coverage Status| |Code Climate| |Python
Versions| |License| |Downloads|

Flask MailGun extension to use the `MailGun <https://mailgun.com>`__
email parsing service for sending and receiving emails.

What it does
------------

Flask-MailGun allows you to configure your connection into the MailGun
api so that you can - Send emails - Set up routes - Handel incoming
emails

Usage
-----

.. code:: python

    from flask_mailgun import MailGun

    mailgun = MailGun()

    # .. later
    mailgun.init_app(app)

    # ..some other time
    @mailgun.on_attachment
    def save_attachment(email, filename, fstream):
        data = fstream.read()
        with open(filename, "w") as f:
            f.write(data)

    # .. even later
    mailgun.create_route('/uploads')

.. |Latest Version| image:: https://img.shields.io/pypi/v/flask-mailgun3.svg
   :target: https://pypi.python.org/pypi/Flask-MailGun3
.. |Build Status| image:: https://travis-ci.org/amey-sam/Flask-MailGun.svg?branch=master
   :target: https://travis-ci.org/amey-sam/Flask-MailGun/builds/
.. |Coverage Status| image:: https://coveralls.io/repos/github/amey-sam/Flask-MailGun/badge.svg?branch=master
   :target: https://coveralls.io/github/amey-sam/Flask-MailGun?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/amey-sam/Flask-MailGun/badges/gpa.svg
   :target: https://codeclimate.com/github/amey-sam/Flask-MailGun
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/flask-mailgun3.svg
   :target: https://pypi.python.org/pypi/Flask-MailGun3
.. |License| image:: https://img.shields.io/pypi/l/Flask-MailGun3.svg
   :target: https://pypi.python.org/pypi/Flask-MailGun3
.. |Downloads| image:: https://img.shields.io/pypi/dm/flask-mailgun3.svg
   :target: https://pypi.python.org/pypi/Flask-Mailgun3
