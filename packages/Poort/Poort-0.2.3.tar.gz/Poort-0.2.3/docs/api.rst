.. _api:

API
===

.. py:currentmodule:: poort


.. autoclass:: poort.Gate

   .. automethod:: setup

.. autoclass:: poort.Request

   .. automethod:: as_dict
   .. automethod:: get_cookie


.. autoclass:: poort.Response

   .. automethod:: set_cookie
   .. automethod:: del_cookie
   .. automethod:: __call__
   .. automethod:: get_status
   .. automethod:: get_body
   .. automethod:: prepare_response
   .. automethod:: respond

.. autofunction:: poort.cli.start
.. autofunction:: poort.cli.stop
.. autofunction:: poort.cli.reload
.. autofunction:: poort.cli.scale
.. autofunction:: poort.cli.status
