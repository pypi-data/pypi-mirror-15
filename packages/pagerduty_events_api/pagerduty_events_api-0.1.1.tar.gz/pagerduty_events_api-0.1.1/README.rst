.. image:: https://travis-ci.org/BlasiusVonSzerencsi/pagerduty-events-api.svg?branch=master
    :target: https://travis-ci.org/BlasiusVonSzerencsi/pagerduty-events-api

.. image:: https://codeclimate.com/github/BlasiusVonSzerencsi/pagerduty-events-api/badges/gpa.svg
    :target: https://codeclimate.com/github/BlasiusVonSzerencsi/pagerduty-events-api
    :alt: Code Climate

.. image:: https://badge.fury.io/py/pagerduty-events-api.svg
    :target: https://badge.fury.io/py/pagerduty-events-api

====================
PagerDuty Events API
====================

Python wrapper for PagerDuty's Events API.

Installation
============

``pip install pagerduty_events_api``

Examples
========

Triggering an alert:
--------------------

::

    import pagerduty_events_api

    service = pagerduty_events_api.PagerdutyService('my_service_key_123')
    incident = service.trigger('some_alert_description')

..

    Please note, that the trigger method of a pagerduty_events_api.PagerdutyService object returns a pagerduty_events_api.PagerdutyIncident instance. Through this instance You can retrieve the identifyer of the triggered incident, acknowledge or resolve it later.

Acknowledging an incident:
--------------------------

::

    import pagerduty_events_api

    incident = pagerduty_events_api.PagerdutyIncident('my_service_key_123', 'my_incident_key456')
    incident.acknowledge()

Resolving an incident:
----------------------

::

    import pagerduty_events_api

    incident = pagerduty_events_api.PagerdutyIncident('my_service_key_123', 'my_incident_key456')
    incident.resolve()


