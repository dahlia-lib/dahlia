Programmatic Dahlia
=================

Dahlia is used by creating a ``Dahlia`` object. It can be used in 2 ways -
using ``Dahlia.convert`` and ``Dahlia.print``.

The difference between the two is ``Dahlia.print`` will print the value while
``Dahlia.convert`` will return it. The underlying usage is the same. For
brevity, the examples will mostly be using ``Dahlia.print``.

.. note:: 

    For a full reference of each code, see :ref:`Format Reference <formatref>`

Formatting is done in Dahlia by prefixing with ``&`` followed by a format code.
(ex: ``&a``) The primary color codes are a number from ``0`` through ``9`` or a
letter from ``a`` through ``g``. To apply the coloring to the background, insert
a ``~`` inbetween. (ex: ``&~a`` )


.. code-block:: python

    from dahlia import Dahlia

    d = Dahlia()
    d.print("&dHello There")
    d.print("&aw&co&3o&6l")
    d.print("&~0&bblack background")

.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre><span class="&d">Hello There</span>
    <span class="&a">w</span><span class="&c">o</span><span class="&3">o</span><span class="&6">l</span>
    <span class="&~0 &b">black background</span>
    </pre>
        </div>
    </div>

Text can also be bold, strikethrough, underline, italic, or removed of formatting.

.. code-block:: python

    from dahlia import Dahlia

    d = Dahlia()
    d.print("&lBold &r&nUnderline&r &oItalics&r &mStrikethrough")


.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre class="&f"><span class="&l">Bold </span><span class="&n">Underline</span><span class="&o"> Italics </span><span class="&m">Strikethrough</span></pre>
        </div>
    </div>


Terminals support a wide range of colors that are not covered by the base format
codes. Dahlia can use hex codes to display a specific color as well.

.. code-block:: python

    from dahlia import Dahlia

    d = Dahlia()
    d.print("use &[#1793d1]ars")


.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre id="data-highlight" class="&f">use <span color="#1793d1">ars</span></pre>
        </div>
    </div>


Dahlia also supports custom markers (`&` being the default):

.. code-block:: python

    from dahlia import Dahlia

    foo = Dahlia(marker="§")  # Has to be a single char!
    foo.print("hi §daster§r!")

.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre id="data-highlight" class="&f">hi <span class="&d">aster</span>!</pre>
        </div>
    </div>


By default, Dahlia automatically adds the ``&r`` code at the end of the string
if it's not present. That can be disabled by enabling the ``no_reset`` flag:

.. code-block:: python

    from dahlia import Dahlia

    foo = Dahlia()
    foo.print("hi &5jane", ":)")
    bar = Dahlia(no_reset=True)
    bar.print("hi &5jane", ":)")

.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre id="data-highlight" class="&f">hi <span class="&5">jane</span> :&#41;</pre>
        <pre id="data-highlight" class="&f">hi <span class="&5">jane :&#41;</span></pre>
        </div>
    </div>


