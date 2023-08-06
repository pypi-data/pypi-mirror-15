python-spark-testing-base
=========================

Base classes to use when writing Python tests with Spark.

Original project
================

This is a fork of the following project to package into Pypi:
https://github.com/holdenk/spark-testing-base

Why?
====

You've written an awesome program in Spark and now its time to write
some tests. Only you find yourself writing the code to setup and tear
down local mode Spark in between each suite and you say to your self:
This is not my beautiful code.

How?
====

::

    pip install spark-testing-base

From now on, you can use the following base classes in your unit tests:

::

    SparkTestingBaseTestCase:

        Basic common test case for Spark. Provides a Spark context as sc.
        For non local mode testing you can either override sparkMaster
        or set the enviroment property SPARK_MASTER for non-local mode testing

    SparkTestingBaseReuse

        Basic common test case for Spark. Provides a Spark context as sc.
        For non local mode testing you can either override sparkMaster
        or set the enviroment property SPARK_MASTER for non-local mode testing

    StreamingTestCase

        Basic common test case for Spark Streaming tests. Provides a
        Spark Streaming context as well as some helper methods for creating
        streaming input and collecting streaming output.
