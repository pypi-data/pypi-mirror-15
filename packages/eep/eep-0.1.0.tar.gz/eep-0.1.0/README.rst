eep
===

Emacs style, point based search-replace for python.

It works by moving a ``point`` and a ``mark`` around in the text,
somewhat similar to how emacs handles its ``buffers``. This becomes
intuitive and easier for *some* text processing tasks which require
usage of *after* and *before* in text.

An example problem is
`here <http://ergoemacs.org/emacs/elisp_process_html.html>`__. Using
``eep``, the equivalent python code is

.. code:: python

      import eep

      text = """<p class='q'>Q: Why</p>\n<p class='a'>Because</p>\n
      <p class='a'>You need to do</p>\n\n
      <p class='q'>Q: How</p>\n
      <p class='a'>Do this</p>\n
      <p class='a'>And that</p>"""

      es = eep.Searcher(text)

      print("Before : \n" + str(es) + "\n\n")

      while es.search_forward("<p class='q'>"):
          es.search_forward("<p class='a'>")
          es.swap_markers()
          es.insert("<div class='a'>\n")

          if es.search_forward("<p class='q'>"):
              es.search_backward("</p>")
              es.swap_markers()
              es.insert("\n</div>")

      es.goto("end")
      es.search_backward("<p class='a'>")
      es.search_forward("</p>")
      es.insert("\n</div>")

      es.goto("start")
      while es.search_forward("<p class='a'>"):
          es.replace("<p>")

      es.goto("start")
      while es.search_forward("<p class='q'>Q: "):
          es.replace("<p class='q'>")

      print("After : \n" + str(es))

.. code:: shell

      Before : 
      <p class='q'>Q: Why</p>
      <p class='a'>Because</p>
      <p class='a'>You need to do</p>

      <p class='q'>Q: How</p>
      <p class='a'>Do this</p>
      <p class='a'>And that</p>


      After : 
      <p class='q'>Why</p>
      <div class='a'>
      <p>Because</p>
      <p>You need to do</p>
      </div>

      <p class='q'>How</p>
      <div class='a'>
      <p>Do this</p>
      <p>And that</p>
      </div>

Usage
-----

-  Install using ``pip install eep``
-  Instantiate a searcher

.. code:: python

      import eep

      es = eep.Searcher("this is a sample text. this is a sentence.")

-  A searcher has two markers for defining regions. A ``point`` moves
   around while searching, replacing, inserting etc. It is the *current*
   position where operations are done.
-  ``mark`` moves after successful forward or backward searches to mark
   matching region with the ``point``.

.. code:: python

      # Search forward for first match from current point
      # Return true if match found
      # Set mark in beginning and point at end
      es.search_forward("th")

      # Search backward for first match from current point
      # Return true if match found
      # Set point in beginning and mark at end
      es.search_backward("th")

      # Replace marked region
      es.replace("dodo")

      # Insert at current point
      es.insert("dodo")

      # Move the point
      es.jump(-3)
      es.goto(34) # also accepts "start" and "end" strings

      # Exchange markers
      es.swap_markers()
