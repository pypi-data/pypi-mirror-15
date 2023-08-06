==============================
scrapy-feedexporter-azure-blob
==============================

.. image:: https://img.shields.io/pypi/v/scrapy-feedexporter-azure.svg
   :target: https://pypi.python.org/pypi/scrapy-feedexporter-azure-blob
   :alt: PyPI Version

.. image:: https://img.shields.io/github/license/undernewmanagement/scrapy-feedexporter-azure-blob.svg
   :target: https://github.com/undernewmanagement/scrapy-feedexporter-azure-blob/blob/master/LICENSE
   :alt: License


scrapy-feedexporter-azure is a `Scrapy Feed Exporter Storage Backend
<http://doc.scrapy.org/en/latest/topics/feed-exports.html#storage-backends>`_
that allows you to export `Scrapy items
<http://doc.scrapy.org/en/latest/topics/items.html>`_ to an Azure Blob Container.

Using scrapy-feedexporter-azure-blob
====================================

Add a the following to your Scrapy settings::

    FEED_STORAGES = {"azure": "scrapy_feedexporter_azure_blob.AzureBlobFeedStorage"}

    FEED_URI = "azure://accountname/container"

    AZURE_ACCOUNT_NAME = "mycrawldata"  # this is the subdomain to https://*.blob.core.windows.net/

    AZURE_ACCOUNT_KEY = "your_account_key"

    AZURE_CONTAINER = 'sites'   # the name of the container (you should have already created it)

    AZURE_FILENAME = 'bob.json'   # the name of the file as it will be in blob storage


Note, you can define all of these settings when you run your crawler with the
``-s`` command line switch:

    ``scrapy crawl <crawler_name> -s AZURE_ACCOUNT_KEY='<account_key>' -s AZURE_ACCOUNT_NAME='<account_name>'``

TODO
====
Have the feed exporter properly parse the FEED_URI string: ``azure://account_name:api_key@container/filename.json``

DEVELOPER NOTES
===============
When deploying to pypi, just use twine
