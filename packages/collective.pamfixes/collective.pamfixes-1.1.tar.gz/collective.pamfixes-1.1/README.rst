collective.pamfixes
===================

This Plone add-on patches the ``AlternateLanguagesViewlet`` from plone.app.multilingual.
The fix addresses `Issue #153 <https://github.com/plone/plone.app.multilingual/issues/153>`_
which can generate broken or inccorect links for the ``rel="alternate"`` links of multilingual pages.
This add-on registers an overriding viewlet with a fix to now generate the correct links.

