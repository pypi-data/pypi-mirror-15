===============================
Netuitive Python Client
===============================

|BuildStatus|_

.. |BuildStatus| image:: https://travis-ci.org/Netuitive/netuitive-client-python.svg?branch=master
.. _BuildStatus: https://travis-ci.org/Netuitive/netuitive-client-python
.. image:: https://coveralls.io/repos/github/Netuitive/netuitive-client-python/badge.svg?branch=master :target: https://coveralls.io/github/Netuitive/netuitive-client-python?branch=master

| The Netuitive Python Client allows you to push data to `Netuitive <https://www.netuitive.com>`_ using Python. Netuitive provides an adaptive monitoring and analytics platform for cloud infrastructure and web applications.

| For more information, check out the `help docs <https://help.netuitive.com>`_ or contact `support <mailto:support@netuitive.com>`_.

The Netuitive Python Client can...

* ...create an `element <https://help.netuitive.com/Content/Performance/Elements/elements.htm>`_ in Netuitive with the following data:
    * Element Name
    * Attributes
    * Tags
    * Metric Samples
    * Element relations
    * Location
    * Metric Tags

* ...create an `event <https://help.netuitive.com/Content/Events/events.htm>`_ in Netuitive with the following data:
    * Element Name
    * Event Type
    * Title
    * Message
    * Level
    * Tags
    * Source

Using the Python Netuitive Client
----------------------------------

Setup the Client
~~~~~~~~~~~~~~~~~

``ApiClient = netuitive.Client(api_key='<my_api_key>')``


Setup the Element
~~~~~~~~~~~~~~~~~~

``MyElement = netuitive.Element()``

Add an Attribute
~~~~~~~~~~~~~~~~~

``MyElement.add_attribute('Language', 'Python')``

Add an Element relation
~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_relation('my_child_element')``

Add a Tag
~~~~~~~~~~

``MyElement.add_tag('Production', 'True')``

Add a Metric Sample
~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('cpu.idle', 1432832135, 1, host='my_hostname')``

Add a Metric Sample with a Sparse Data Strategy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.zero', 1432832135, 1, host='my_hostname', sparseDataStrategy='ReplaceWithZero')``

Add a Metric Sample with unit type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', unit='requests/s')``

Add a Metric Sample with utilization tag
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.requests', 1432832135, 1, host='my_hostname', tags=[{'utilization': 'true'}])``

Add a Metric Sample with min/max values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.add_sample('app.percent_used', 1432832135, 50, host='my_hostname', unit='percent', min=0, max=100)``

Send the Samples
~~~~~~~~~~~~~~~~~

``ApiClient.post(MyElement)``

Remove the samples already sent
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``MyElement.clear_samples()``

Create an Event
~~~~~~~~~~~~~~~~

``MyEvent = netuitive.Event(hst, 'INFO', 'test event','this is a test message', 'INFO')``

Send the Event
~~~~~~~~~~~~~~~

``ApiClient.post_event(MyEvent)``

Check that our local time is set correctly (returns True/False)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ApiClient.time_insync()``

Example
----------
The below example sets up the Netuitive Python client, creates an element ("MyElement") with attributes, a relationship, and tags and then passes in some samples. After the element is posted, the samples are cleared, an event is created and posted.
::

    import netuitive
    import time

    ApiClient = netuitive.Client(api_key='aaaa9956110211e594444697f922ec7b')

    MyElement = netuitive.Element()

    MyElement.add_attribute('Language', 'Python')
    MyElement.add_attribute('app_version', '7.0')

    MyElement.add_relation('my_child_element')

    MyElement.add_tag('Production', 'True')
    MyElement.add_tag('app_tier', 'True')

    timestamp = int(time.mktime(time.gmtime()))
    MyElement.add_sample('app.error', timestamp, 1, host='appserver01')
    MyElement.add_sample('app.request', timestamp, 10, host='appserver01')

    ApiClient.post(MyElement)

    MyElement.clear_samples()

    MyEvent = netuitive.Event('appserver01', 'INFO', 'test event','this is a test message', 'INFO')

    ApiClient.post_event(MyEvent)

    if ApiClient.time_insync():
        print('we have time sync with the server')

Copyright and License
---------------------

Copyright 2015-2016 Netuitive, Inc. under [the Apache 2.0 license](LICENSE).
