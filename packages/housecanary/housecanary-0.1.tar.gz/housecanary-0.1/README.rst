HouseCanary API Python Client
=============================

The `HouseCanary <http://www.housecanary.com>`_ API Python Client provides an easy interface to call the HouseCanary API.


API documentation
-----------------

Full documentation is available at https://api-docs.housecanary.com

Installation
------------

To install:

::

    pip install housecanary

Basic Usage
-----------

.. code:: python

    import housecanary
    client = housecanary.ApiClient("my_api_key", "my_api_secret")
    result = client.property.value(("85 Clay St", "02140"))

    # result is an instance of housecanary.response.Response
    print result.json()

Authentication
--------------

When you create an instance of an ApiClient, you need to give it your
API key and secret. You can manage these in your settings page at
https://valuereport.housecanary.com/#/settings.

You can pass these values to the ApiClient constructor:

.. code:: python

    client = housecanary.ApiClient("my_api_key", "my_api_secret")

Alternatively, instead of passing in your key and secret to the
constructor, you can store them in the following environment variables:

-  HC\_API\_KEY
-  HC\_API\_SECRET

Creating an instance of ApiClient with no arguments will read your key
and secret from those environment variables:

.. code:: python

    client = housecanary.ApiClient()

Usage Details
-------------

Endpoint methods
~~~~~~~~~~~~~~~~

The ApiClient class provides a ``property`` wrapper which contains
various methods for calling the different endpoints of the HouseCanary
API:

-  **analyze**
-  **underwrite**
-  **value**
-  **value\_report**

More wrapper objects may be added to ApiClient later like “zipcode” and
“lat\_lng”.

**Args:**
     

All of the above endpoint methods (except for ``value_report``) take an
``address_data`` argument. ``address_data`` can be in one of two forms:

A Json formatted list like:

.. code:: python

    [{"address":"82 County Line Rd", "zipcode":"72173", "meta":"extra info"}]

Or, a list of (address, zipcode, meta) tuples like:

.. code:: python

    [("82 County Line Rd", "72173", "extra info")]

The “meta” field is optional. If you’re only providing one address, you
can provide a tuple on it’s own:

.. code:: python

    ("82 County Line Rd", "72173")

All of the endpoint methods of this class return a Response object or
the output of a custom OutputGenerator if one was specified in the
constructor.

**Example:**
        

.. code:: python

    client = housecanary.ApiClient()
    result = client.property.value([("85 Clay St", "02140"), ("82 County Line Rd", "72173")])

**Value Report:**
             

The ``value_report`` method behaves differently than the other endpoint
methods. It only supports one address at a time, and it takes some
extra, optional parameters:

Args: 
    - *address* (str) 
    - *zipcode* (str)

Kwargs: 
    - *report\_type* - “full” or “summary”. Optional. Default is "full"
    - *format\_type* - "json", "pdf" or "all". Optional. Default is "json"

**Example:**
        

.. code:: python

    client = housecanary.ApiClient()
    # get Value Report in JSON format with "summary" report_type.
    result = client.property.value_report("85 Clay St", "02140", "summary", "json")
    # print the JSON output
    print result.json()

    # get Value Report in PDF format with "full" report_type.
    result = client.property.value_report("85 Clay St", "02140", format_type="pdf")
    # result is binary data of the PDF.

Learn more about the various endpoints in the `API docs. <https://api-docs.housecanary.com/#endpoints>`_


Custom endpoint for bundles
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You may want to retrieve data for a different combination of components
not provided in the standard endpoints. In this case, you can use the
``custom`` method. The ``custom`` method takes an ``address_data``
argument just like the other endpoint methods. Pass in a list of
component names as the second argument.

**Example:**
        

.. code:: python

    client = housecanary.ApiClient()
    result = client.property.custom(("85 Clay St", "02140"), ["property/value", "property/census", "property/details"])

**Note**: The list of components you provide to the ``custom`` method
must include at least one of: “property/value”, “property/rental\_value”
or “property/value\_forecast”. Otherwise, the API will return a 403
response.

You can find the full list of available components in the `API
docs. <https://api-docs.housecanary.com/#components>`__

You may receive a bundle name from a HouseCanary support representative.
A bundle is a predefined group of components. You can use a bundle with
the ``custom`` method by passing the bundle name to the ``bundle``
argument.

**Example:**
        

.. code:: python

    result = client.property.custom(("85 Clay St", "02140"), bundle="bundle1")

Response
~~~~~~~~

Response is a base class for encapsulating an HTTP response from the
HouseCanary API.

**Properties:**
           

-  **endpoint\_name** - Gets the component name of the original request
-  **response** - Gets the underlying response object. ###### Methods:
-  **json()** - Gets the body of the response from the API as json.
-  **has\_object\_error()** - Returns true if any requested objects had
   a business logic error, otherwise returns false.
-  **get\_object\_errors()** - Gets a list of business error message
   strings for each of the requested objects that had a business error.
   If there was no error, returns an empty list.
-  **objects()** - Overridden in subclasses.

PropertyResponse
~~~~~~~~~~~~~~~~

A subclass of Response, this is returned for all property components
except for ``value_report``.

**Methods:**
        

-  **objects()** - Gets a list of Property objects for the requested
   properties, each containing the object’s returned json data from the
   API.
-  **properties()** - An alias for the objects() method.

HouseCanaryObject
~~~~~~~~~~~~~~~~~

Base class for various types of objects returned from the HouseCanary
API. Currently, only the Property subclass is implemented.

**Properties:**
           

-  **component\_results** - a list of ComponentResult objects that
   contain data and error information for each component requested for
   this HouseCanaryObject.

**Methods:**
        

-  **has\_error()** - Returns a boolean of whether there was a business
   logic error fetching data for any components for this object.
-  **get\_errors()** - If there was a business error fetching data for
   any components for this object, returns the error messages.

Property
~~~~~~~~

A subclass of HouseCanaryObject, the Property represents a single
address and it’s returned data.

**Properties:**
           

-  **address**
-  **zipcode**
-  **zipcode\_plus4**
-  **address\_full**
-  **city**
-  **country\_fips**
-  **lat**
-  **lng**
-  **state**
-  **unit**
-  **meta**

**Example:**
        

.. code:: python

    result = client.property.value(("123 Main St", "01234", "meta information"))
    p = result.properties()[0]
    print p.address
    # "123 Main St"
    print p.zipcode
    # "01234"
    print p.meta
    # "meta information"
    value_result = p.component_results[0]
    print value_result.component_name
    # 'property/value'
    print value_result.api_code
    # 0
    print value_result.api_code_description
    # 'ok'
    print value_result.json_data
    # {u'value': {u'price_upr': 1575138.0, u'price_lwr': 1326125.0, u'price_mean': 1450632.0, u'fsd': 0.086}}
    print p.has_error()
    # False
    print p.get_errors()
    # []

ValueReportResponse
~~~~~~~~~~~~~~~~~~~

A subclass of Response, this is the object returned for the
``value_report`` endpoint when “json” format\_type is used. It simply
returns the JSON data of the Value Report.

**Example:**
        

.. code:: python

    result = client.property.value_report("123 Main St", "01234")
    print result.json()

License
-------

This API Client Library is made available under the MIT License:

The MIT License (MIT)

Copyright (c) 2016 HouseCanary, Inc

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For the avoidance of doubt, the above license does not apply to
HouseCanary’s proprietary software code or APIs, or to any data,
analytics or reports made available by HouseCanary from time to time,
all of which may be licensed pursuant to a separate written agreement