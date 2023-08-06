LocalNote
=========

|Gitter| |Python27| `Chinese Version <https://github.com/littlecodersh/LocalNote/blob/master/README.md>`__

LocalNote enables you to use evernote in the local-file way.

Popular markdown format is supported and can be perfectly performed in evernote (the download format will remain as .md instead of .html).

Majority of notes in evernote can also be translated into markdown format easily.

LocalNote is also available on three platforms, which ensure that linux users can also have a good experience with evernote.

You are welcomed to join this project on `Github <https://github.com/littlecodersh/LocalNote>`__.

**Screenshot**

|GifDemo|

Video is `here <http://v.youku.com/v_show/id_XMTU3Nzc5NzU1Ng==>`__.

**Installation**

.. code:: bash

    pip install localnote

**Usage**

Commonly used commands

.. code:: bash

    # initialize the root folder, please use this in an empty folder
    localnote init
    # download your notes from your evernote to your computer
    localnote pull
    # show the difference between your local notes and online notes
    localnote status
    # upload your notes from your computer to your evernote
    localnote push
    # translate html documents into markdown formats
    localnote convert file_need_convert.html

Storage format

- A folder in the root folder means a notebook
- A document, folder as well, in notebook folder means a note
- A note can contain main document only or have attachments in any format.
- Main document of a note must be a `.md` or `.html` file, its file name will be used as note name.

Example file tree

::

    Root
        My default notebook 
            My first notebook.html
            My second notebook.html
        Attachment notebook
            My third notebook
                My third notebook.md
                Packed documents.zip
                Note of packing.txt
        Empty notebook

**FAQ**

Q: I have an error `errorCode=19`, how should I deal with it?

A: This is the hourly limit of evernote, you just need to wait for an hour. The whole Exception is `evernote.edam.error.ttypes.EDAMSystemException: EDAMSystemException(errorCode=19, rateLimitDuration=1039, _message=None)`. Login will also be limited in the hour, so warning about not loged in will be shown.

Q: Will the first pull take a long time?

A: It depands how big your files are, the downloading speed is about 200k/s.

Q: How to preview markdown files locally?

A: You need a web browser plugin. Take Chrom for example, it's `Markdown Preview Plus <https://chrome.google.com/webstore/detail/markdown-preview-plus/febilkbfcbhebfnokafefeacimjdckgl>`__.

**Comments**

If you have any question or suggestion, you can discuss with me in this `Issue <https://github.com/littlecodersh/LocalNote/issues/1>`__ .

Or you may contact me on gitter: |Gitter|

.. |Python27| image:: https://img.shields.io/badge/python-2.7-ff69b4.svg
.. |Gitter| image:: https://badges.gitter.im/littlecodersh/LocalNote.svg
    :target: https://github.com/littlecodersh/ItChat/tree/robot
.. |GifDemo| image:: http://7xrip4.com1.z0.glb.clouddn.com/LocalNoteDemo.gif
