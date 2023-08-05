1.1.1 (2016-05-05)
==================
- Include missing migrations into package.

1.1.0 (2015-10-16)
==================
- Corrected a situation where project migrating database from old version not using django-autoadmin would have problem logging in.
- Added a test project
- Code coverage is now 100%
- Added tox test support
- Setting overrides now work all the time
- django-autoadmin is now tested against Python 2.7, 3.2, 3.3, 3.4, Django 1.7 and 1.8
- Removed all PEP8 warnings
- All autoadmin code was moved from the management command to the AutoAdminSingleton manager

1.0.1 (2015-06-14)
==================

- No changes, just a version bump as required by PyPI

1.0.0 (2015-06-14)
==================

- Update included partial template
- Django admin interface enabled
- Drop support for Django < 1.6
- Adds support Django >= 1.7
- Autoadmin user is no longer created after database migration
- Add new createautoadmin management command
- Uses Django's own createsuperuser management command
- Adds Django native database migrations
- Uses AppConfig to about running code during import
- Adds supports for custom User models
- ENABLE setting removed
- Default email changed to autoadmin@example.com

0.5.0 (2014-08-25)
==================

- Initial release
