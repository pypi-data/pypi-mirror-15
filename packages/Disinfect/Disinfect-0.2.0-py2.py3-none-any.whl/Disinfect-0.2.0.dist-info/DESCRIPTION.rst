Disinfect: Destroy bad input.
==================================================================

.. begin

Disinfect allows you to validate and sanitize incoming data.

* Free software: MIT license
* Documentation: http://pythonhosted.org/disinfect

A quick example:

.. code-block:: python

   import disinfect as d

   mapping = d.Mapping({
       'first': d.String(),
       Field('infix', default=''): d.String(min_len=0,
                                            max_len=40),
       'last': d.String(),

       'addresses': d.ListOf(Mapping({
           'zipcode': d.String(min_len=5, max_len=5),
           'housenumber': d.Int(min_value=1),
       }))
   })

   user = mapping({
       'first': 'Nils',
       'last': 'Corver',
       'addresses': [
           {'zipcode': '71486', 'housenumber': '49'},
           {'zipcode': '59546', 'housenumber': '709'},
       ]
   })

   assert user == {
       'first': 'Nils',
       'infix': '',
       'last': 'Corver',
       'addresses': [
           {'zipcode': '71486', 'housenumber': 49},
           {'zipcode': '59546', 'housenumber': 709},
       ]
   }

   with raises(d.MultiValueError) as exc:
       mapping({})

   assert exc.value.to_dict() == {
       'first': 'Field is required.',
       'last': 'Field is required.',
       'addresses': 'Field is required.',
   }


Features
--------

* TODO

Authors
-------

``Disinfect`` is written and maintained by
`Nils Corver <nils@corverdevelopment.nl>`_.

A full list of contributors can be found in
`GitHub's overview <https://github.com/corverdevelopment/disinfect/graphs/contributors>`_.


