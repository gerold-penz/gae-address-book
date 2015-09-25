###############################################
Google App Engine - Address Book - Data Backend
###############################################


=============
Version 0.1.9
=============

2015-09-25

- New API function: *start_refresh_index*.


=============
Version 0.1.8
=============

2015-09-18

- New Function: *get_categories*

- New Fields *xxx_char1*


=============
Version 0.1.7
=============

2015-09-18

- Filter changed


=============
Version 0.1.6
=============

2015-09-17

- Tag-Items added

- Added three new filters:

  - filter_by_category_items
  - filter_by_tag_items
  - filter_by_business_items


=============
Version 0.1.5
=============

2015-09-16

- Saving one address (not finished yet)


=============
Version 0.1.4
=============

2015-09-15

- New model for address changes: AddressHistory

- *get_addresses* now accept the parameter *order_by* for sorting the result.

- Filtering


=============
Version 0.1.3
=============

2015-09-08

- New test-security-settings added

- Computed properties: birthday, age


=============
Version 0.1.2
=============

2015-09-07

- Address-model: *to_dict()* returns a shortned dictionary

- *get_addresses()* shortened

- New function *get_address()*

- *get_address* returns one record no list.


=============
Version 0.1.1
=============

2015-09-04

- New *python-jsonrpc*-Version added

- GZIP for JSON-RPC-Requests now allowed

- New *get_addresses*-Funktion to request addresses in pages


=============
Version 0.1.0
=============

2015-09-03

- `appname` --> `APPNAME`

- Bei Fehler wird ein E-Mail an Gerold gesendet


=============
Version 0.0.3
=============

2015-09-02

- JSON-RPC-API:

  - Added *get_info()*-Function

  - Create-Function finished and tested


=============
Version 0.0.2
=============

2015-09-01

- Address datamodel created

- *security.ini* for authentification and authorization

- *create*-function created

- Tests

- Address datamodel changed


=============
Version 0.0.1
=============

2015-08-31

- Initial import

- Program structure created

- Help for JSON-RPC-API added


