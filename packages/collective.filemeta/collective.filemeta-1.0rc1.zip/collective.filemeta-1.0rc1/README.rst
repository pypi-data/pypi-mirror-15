.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

==============================================================================
collective.filemeta
==============================================================================

.. image:: https://travis-ci.org/collective/collective.filemeta.svg
    :target: https://travis-ci.org/collective/collective.filemeta

Background information
-----------------------

When for example MS Office or PDF documents are stored in Plone as normal File content,
document metadata embedded in the documents is not used. Such metadata is embedded
inside the files in various type-specific formats, and might include information such as
title, description and keywords, or EXIF/IPTC metadata for images. Nor does Plone provide
a screenshot or cover page thumbnail of the document.

This packages aims to provide those missing features in a generic, pluggable manner.

Note that in addition to this package, you need additional packages to provide the actual
file type - specific metadata extraction, such as:

- Products.OpenXml for MS Office document support
- collective.pdfdocument for PDF support


Features provided
------------------

- Generic pluggable mechanism to retrieve metadata from different file types, update
  content with it, and even round-trip the metadata back to the file from Plone content,
  if needed

- Behavior to toggle the mechanism by content type

- An example optional 'Document File' Dexterity content type that gets its metadata and
  cover image automatically copied over from the uploaded document file

- Optionally enhanced built-in File content type so that it gets it metadata updated
  from uploaded file (including cover image)

- A nicer default view (used both for the example type & enhanced File)

Features not provided
----------------------

- viewing the document contents

- indexing of documents (would be a good fit though)

- asynchronous operation


Note on metadata and cover images
------------------------------------

Usually people don't bother with document metadata so prior to uploading, you should check
the document properties.

For MS Office docs, make sure that the "store preview" option is selected, before saving
the document. PDFs have no embedded cover image; for them,  collective.pdfdocument
converts the first page of the PDF into a PNG cover image.


Implementation notes
---------------------

Metadata is processed by a subscriber that attemtps to retrieve the metadata using a 'IFileMetaProvider' utility whose name matches the primary file field mime type. If the
metadata can be extracted from file, it is copied over by another 'IContentMetaUpdater'
utility whose name matches the metadata label (such as "title"), or metadata standard or
format (such as "dc", for Dublin Core, or "exif"). There's also a 'IFileMetaUpdater'
interface for updating the file when someone updates the metadata of the Plone content
object.


Installation
------------

Install collective.filemeta by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.filemeta


and then running ``bin/buildout``. Remember that you will also need some additional
packages that provide the file type -specific extraction of document file metadata. For
MS Office OpenXML and PDF support, the buildout would have::

    [buildout]

    ...

    eggs =
        collective.filemeta
        Products.OpenXml
        collective.pdfdocument


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.filemeta/issues
- Source Code: https://github.com/collective/collective.filemeta


Support
-------

If you are having issues, please submit them to tracker or contact the author.

License
-------

The project is licensed under the GPLv2.
