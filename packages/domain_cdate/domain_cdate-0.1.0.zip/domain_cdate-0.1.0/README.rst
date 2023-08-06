Domain creation date extractor
==============================

.. code-block:: python

    import asyncio
    import domain_cdate

    loop = asyncio.get_event_loop()
    coro = domain_cdate.creation_date('google.com')
    print(loop.run_until_complete(coro))
    loop.close()
