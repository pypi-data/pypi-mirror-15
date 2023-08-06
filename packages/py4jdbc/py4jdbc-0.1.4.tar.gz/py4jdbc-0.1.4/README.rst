Py4jdbc
===========

.. image:: https://travis-ci.org/massmutual/py4jdbc.svg
   :target: https://travis-ci.org/massmutual/py4jdbc

This repo aspires to be a (partially) `dbapi 2.0 <https://www.python.org/dev/peps/pep-0249/>`_ compliant interface to JDBC. It's similar to `JayDeBeAPI <https://github.com/baztian/jaydebeapi>`_, but uses a much more efficient JVM backend process implemented with Py4j instead of JPype.

Install py4jdbc
++++++++++++++++

Py4jdbc will automatically add its jar file to your $CLASSPATH if installed from githib with pip -install e::

    pip install -e git+git@github.com:massmutual/py4jdbc.git#egg=py4jdbc
    
You can also pip install py4jdbc, but you'll have to manually dig up the jar file and add it to your $CLASSPATH.

Example
++++++++++++

A simple example that starts a JVM subprocess::

    from py4jdbc import connect

    conn = connect("jdbc:postgresql://localhost/postgres, user="cow", password="moo")
    cur = conn.cursor()
    cur.execute("select 1 as cow;")
