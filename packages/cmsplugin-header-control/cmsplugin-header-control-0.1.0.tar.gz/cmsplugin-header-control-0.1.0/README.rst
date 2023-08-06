CMSPlugin Header Control
========================

A plugin that manages HTTP headers for its children plugins.

Requirements
------------

This addon will have no affect at all in CMS versions prior to 3.3.0.


Installation
------------

Aldryn
~~~~~~

TODO

Other installations
~~~~~~~~~~~~~~~~~~~

1. Install the package via `pip install cmsplugin-header-control`;
2. Add `cmsplugin_header_control` to your `INSTALLED_APPS` in the settings.py file for your project;
3. Migrate with `python manage.py migrate cmsplugin_header_control`.


Usage
-----

To use CMSPlugin Header Control, add the "Header Control" plugin to a 
placeholder. The plugin has essentially two settings: cache expiration and 
VARY headers. Add additional plugins "inside" this plugin.

