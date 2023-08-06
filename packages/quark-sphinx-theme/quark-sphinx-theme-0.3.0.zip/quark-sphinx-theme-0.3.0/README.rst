========================================
Quark: a Sphinx theme for QTextBrowser
========================================

About
=====

Quark is a Sphinx theme specifically designed to look and work well within the
limitations of the Qt toolkit's ``QTextBrowser``.

This theme was originally designed for the bundled manual of `SpeedCrunch`_.

.. _SpeedCrunch: http://speedcrunch.org


Installation
============

* ``pip install quark-sphinx-theme``
* In your ``conf.py``::

    import quark_sphinx_theme
    html_theme_path = [quark_sphinx_theme.get_path()]
    html_theme = 'quark'
    # To enable more QTextBrowser-compatible HTML generation:
    extensions = ['quark_sphinx_theme.ext.html_rewrite']


Changelog
=========

* quark-sphinx-theme 0.3 *(2016-05-22)*

  - Remove ``hide_sidebar_in_index`` option.
  - Fix styling of index pages.
  - The ``quark_sphinx_theme.ext.html_compat`` extension has been renamed to
    ``quark_sphinx_theme.ext.html_rewrite``. The old name remains supported for
    backwards compatibility.
  - The ``html_rewrite`` extension now supports wrapping admonitions in tables,
    allowing for more styling options. The theme has been updated to take
    advantage of this. Admonitions, topics, and sidebars look very different and
    much better. If ``html_rewrite`` is not enabled, a fallback style will be
    used for these.
  - ``html_rewrite`` supports wrapping literal blocks in tables. If enabled,
    this provides better styling for Pygments styles with non-white backgrounds.
  - Smaller design changes:

    - Don't use background color on code elements in headings and normal links.
    - Display terms in definition lists in bold.
    - Remove left and top margins for definition list bodies.
    - Switch default code color scheme to 'lovelace'.

* quark-sphinx-theme 0.2.1 *(2016-03-02)*

  - Change license to 2-clause BSD (in practice, it's the same thing).

* quark-sphinx-theme 0.2.0 *(2016-02-28)*

  - Add ``quark_sphinx_theme.ext.html_compat`` extension.
  - Add styling for citations, footnotes, table captions, and ``rubric``
    directives.

* quark-sphinx-theme 0.1.2 *(2016-02-27)*

  - Fix compatibility with Jinja2 2.3.

* quark-sphinx-theme 0.1.1 *(2016-02-24)*

  - Fix spacing of navigation links.

* quark-sphinx-theme 0.1.0 *(2016-02-24)*

  - Initial release.
