====================================
 Allabaster is embeddable Alabaster
====================================

Changes from Alabaster
======================

* All these fancy sidebars and footers were stripped down, as well,
  as html head and body tags. Now theme generates not complete html
  pages, but html fragments. It's intended usage – to insert these
  fragments into other html pages.
* CSS code was modified to decrease chance of interference with
  css rules of the main site.
* Breadcrumbs were added to simplify navigation.

.. warning:: The rest of the page is not reworked yet, and copied from Alabaster.

Alabaster is a visually (c)lean, responsive, configurable theme for the `Sphinx
<http://sphinx-doc.org>`_ documentation system. It is Python 2+3 compatible.

It began as a third-party theme, and is still maintained separately, but as of
Sphinx 1.3, Alabaster is an install-time dependency of Sphinx and is selected
as the default theme.

Live examples of this theme can be seen on `this project's own website
<http://alabaster.readthedocs.io>`_, `paramiko.org <http://paramiko.org>`_,
`fabfile.org <http://fabfile.org>`_ and `pyinvoke.org <http://pyinvoke.org>`_.

For more documentation, please see http://alabaster.readthedocs.io.

.. note::
    You can install the `development version
    <https://github.com/bitprophet/alabaster/tarball/master#egg=alabaster-dev>`_
    via ``pip install alabaster==dev``.
