###############################################
Google App Engine - Address Book - Data Backend
###############################################


ToDo: Security: Authorization: *common.authorization*


=============
Version 0.4.1
=============

2018-03-26

- Test der Strukturanpassung


=============
Version 0.4.0
=============

2017-06-23

- Strukturanpassung für neuen Upload in die App Engine.


=============
Version 0.3.4
=============

2017-04-26

- Tag-Items und Category-Items werden jetzt zum Cache hinzugefügt, wenn
  Tags oder Categories zu einer Adresse hinzugefügt werden.


=============
Version 0.3.3
=============

2017-04-20

- Cron-Job für das Backup automatisiert


=============
Version 0.3.2
=============

2017-02-14

- Versuch einen Fehler beim Erstellen des Indexes auszubessern


=============
Version 0.3.1
=============

2017-01-20

- New API-functions: *add_categories()* and *delete_categories()*

- New API-functions: *add_tags()* and *delete_tags()*


=============
Version 0.3.0
=============

2016-11-14

- Api: *get_addresses_for_iteration()*


==============
Version 0.2.12
==============

2016-11-14

- Dev-API-Tests


==============
Version 0.2.11
==============

2016-11-10

- Free defined fields: *value_type* added


==============
Version 0.2.10
==============

2016-09-15

- Index fields append


=============
Version 0.2.9
=============

2016-09-13

- Dev-Api added


=============
Version 0.2.8
=============

2016-07-06

- Index for tag_items changed


=============
Version 0.2.7
=============

2016-06-30

- Bug fixed: IndexError: string index out of range

- Address-model: "indexed = false" removed

- Free-Defined-Items are now *ndb.TextProperty*-Fields

- New field: *FreeDefinedField.visible*


=============
Version 0.2.6
=============

2016-06-29

- Bug fixed: Error if no search index

- New Error QUERY_ERROR defined


=============
Version 0.2.5
=============

2016-06-28

- After deleting an address: address will removed from search index, too

- New Api-function: *get_search_index_fieldnames()*


=============
Version 0.2.4
=============

2016-06-27

- Search index: "_char1"-Fields added

- JsonRPC-getAddresses() --> common.addresses.get_addresses_by_search()


=============
Version 0.2.3
=============

2016-05-23

- FreeDefinedFieldHistory-model deleted

- Tag-Items, Business-Items and Category-Items are now cached

- Deletion of addresses now works with a new model

- Cron-Jobs added

- New functions added:

    - delete_all_addresses
    - start_delete_all_addresses
    - delete_all_search_indexes
    - start_delete_all_search_indexes


=============
Version 0.2.2
=============

2016-05-22

- New model: NamedValue contains a simple key-value-store.

- Tag items, now have an own module.

- Cached tag items

- *common.named_values.get_value()* now uses the key to fetch values from database.


=============
Version 0.2.1
=============

2016-05-19

- Huge changes in the program-structure


=============
Version 0.2.0
=============

2016-05-17

- Webapp2 added (ZIP file).


==============
Version 0.1.23
==============

2016-05-13

- Search-Index: Anniversary-Date --> ISO-String


==============
Version 0.1.22
==============

2016-05-09

- URL: "http" concatenated


==============
Version 0.1.21
==============

2016-05-06

- Bugs


==============
Version 0.1.20
==============

2016-05-04

- Get and set free defined fields works, now.

- New: *FreeDefinedField.group*


==============
Version 0.1.19
==============

2016-05-03

- New: FreeDefinedField-Model

- Default authorizations added

- JsonRpc-functions for free defined fields added

- Documentation added

- *index.yaml* added


==============
Version 0.1.18
==============

2016-04-26

- AgreementItems

- JournalItems are now without explicit date

- The Address model has got the new field *free_defined_items*, which allows
  to add several free defined values to the address.


==============
Version 0.1.17
==============

2016-04-08

- Python-JsonRPC-Version 0.9.0

- On address creation: CT will no set correct

- Only save not emtpy item_lists (notes, journal, ...)


==============
Version 0.1.16
==============

2016-04-07

- Beim Speichern der Adresse werden alte CT und CU übernommen, wenn es eine UUID gibt.

- Beim Speichern der Adresse wird jetzt auf None geprüft um auch leere Listen
  speichern zu können.

- Saving ET and EU corrected.


==============
Version 0.1.15
==============

2016-03-22

- Datetime-serializable JSON-module (jsonx) added

- *delete_address*-function: *force*-parameter added

- New Version of *pyjsonrpc.zip* added

- New Version of *cherrypy.zip* added

- New Version of *mako.zip* added

- Datamodel changed: *uid*-fields added


==============
Version 0.1.14
==============

2016-03-21

- New API-function: *delete_address*


==============
Version 0.1.13
==============

2015-10-06

- New API-function: *search_addresses*


==============
Version 0.1.12
==============

2015-10-05

- Trials with Google search

- Adds a document to the search index, every time an address will saved.


==============
Version 0.1.11
==============

2015-09-29

- *get_addresses*: Added filter parameters.


==============
Version 0.1.10
==============

2015-09-28

- API changed: *create_address*: *_list*-parameters replaced with *_items*.

- New functions: *get_business_items*, *get_tag_items*


=============
Version 0.1.9
=============

2015-09-25

- New API function: *start_refresh_index*.

- API function *get_addresses* returns now a dictionary

- New function *save_address*.


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


