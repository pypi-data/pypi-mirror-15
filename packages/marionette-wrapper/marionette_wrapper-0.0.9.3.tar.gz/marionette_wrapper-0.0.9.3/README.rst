==================
marionette-wrapper
==================
.. image:: https://img.shields.io/pypi/l/marionette-wrapper.svg
   :target: https://github.com/mozilla-services/marionette-wrapper/blob/master/LICENSE
   :alt: License
.. image:: https://travis-ci.org/mozilla-services/marionette-wrapper.svg?branch=master
    :target: https://travis-ci.org/mozilla-services/marionette-wrapper
.. image:: https://img.shields.io/github/issues-raw/mozilla-services/marionette-wrapper.svg
   :target: https://github.com/mozilla-services/marionette-wrapper/issues
   :alt: Issues
.. image:: https://img.shields.io/requires/github/mozilla-services/marionette-wrapper.svg
   :target: https://requires.io/github/mozilla-services/marionette-wrapper/requirements/?branch=master
   :alt: Requirements

Overview
--------
This package contains a class that serves as a base class for page object classes. The base class wraps commonly used
`Selenium WebDriver <http://docs.seleniumhq.org/docs/03_webdriver.jsp>`_ functionality into readable functions and gives a clean API for page objects to consume.

Installation
------------

:code:`python setup.py develop`

Usage
-----

To use the base class, you would create a page object class that inherits from the base class found in base.py. View the API Reference
for the exact calls that can be made in the API.

.. code-block:: python

    from marionette-wrapper.base import Base

    class PageObject(Base):
        #code

Run Tests
~~~~~~~~~
The sample test included with this package uses pytest to run the test. To invoke the test run the following commmand:

:code:`py.test --capture=sys tests/test_marionette_wrapper_commands.py`

API Examples For Common Functionality
-------------------------------------

This reference shows the marionette-wrapper API call and it's equivalent Selenium counterpart.

Launch
~~~~~~
`This command is to launch the webpage only after checking if the URL is properly formed.`

.. code-block:: python

    if url is not None:
        regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)'
            r'+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if regex.match(url):
            self.marionette.navigate(url)
        else:
            raise ValueError('Url is malformed.')

Click Element
~~~~~~~~~~~~~
`This command is to click on the given element.`

.. code-block:: python

    # marionette-wrapper
    self.click_element(by, locator)

    # Selenium WebDriver
    self.marionette.find_element(by, locator).click()

Wait For Element Present
~~~~~~~~~~~~~~~~~~~~~~~~
`This command is to check that an element exists in the DOM. Does not necessarily have to be visible.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_present(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(expected.element_present(by, locator))

Wait For Element Not Present
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`This command waits for an element to leave the DOM. If this does not happen before the timeout expires, an exception is thrown.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_not_present(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(expected.element_not_present(by, locator))

Wait For Element Displayed
~~~~~~~~~~~~~~~~~~~~~~~~~~
`This command waits for an element display itself on the page. If this does not happen before the timeout expires, an exception is thrown.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_displayed(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(
        expected.element_displayed(
            Wait(self.marionette).until(
                expected.element_present(by, locator))))

Wait For Element Not Displayed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`This command waits for an element to become invisible on the page. If this does not happen before the timeout expires, an exception is thrown.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_not_displayed(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(
        expected.element_not_displayed(
            Wait(self.marionette).until(
                expected.element_present(by, locator))))

Wait For Element Enabled
~~~~~~~~~~~~~~~~~~~~~~~~
`This command waits for an element to become enabled. If this does not happen before the timeout expires, an exception is thrown.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_enabled(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(
            expected.element_enabled(lambda m: m.find_element(by, locator)))

Wait For Element Not Enabled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
`This command waits for an element to become disabled. If this does not happen before the timeout expires, an exception is thrown.`

.. code-block:: python

    # marionette-wrapper
    self.wait_for_element_not_enabled(by, locator)

    # Selenium WebDriver
    Wait(self.marionette).until(
            expected.element_not_enabled(lambda m: m.find_element(by, locator)))

Is Element Present
~~~~~~~~~~~~~~~~~~
`This command is to return a boolean as to whether an element exists in the DOM. Does not have to be visible.`

.. code-block:: python

    # marionette-wrapper
    self.is_element_present(by, locator)

    # Selenium WebDriver
    try:
        self.marionette.find_element(by, locator)
        return True
    except NoSuchElementException:
        return False

Is Element Displayed
~~~~~~~~~~~~~~~~~~~~
`This command is to return a boolean as to whether an element is present and visible on the page.`

.. code-block:: python

    # marionette-wrapper
    self.is_element_displayed(by, locator)

    # Selenium WebDriver
    try:
        return self.marionette.find_element(by, locator).is_displayed()
    except NoSuchElementException:
        return False
