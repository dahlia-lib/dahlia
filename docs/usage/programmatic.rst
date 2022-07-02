Programmatic Wool
=================

The two ways wool can be used with Python is with the functions :func:`~wool.wool` and :func:`~wool.wprint`.

The difference between the two is :func:`~wool.wprint` will print the value while :func:`~wool.wool` will return it. 
The underlying usage is exactly the same. For brevity the examples will mostly be using ``wprint``.

.. note:: 
    
    For a full reference of each code, see :ref:`Format Reference <formatref>`

Formatting is done in wool by prefixing with ``&`` followed by a format code. (ex: ``&a``)
The basic color codes are a number from ``0`` through ``9`` or letter from ``a`` through ``g``.
To apply the coloring to the background, insert a ``~`` between. (ex: ``&~a`` )


.. code-block:: python

    from wool import wprint
    wprint("&dHello There")
    wprint("&aw&co&3o&6l")
    wprint("&~0&bblack background")

.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre><span class="&d">Hello There</span>
    <span class="&a">w</span><span class="&c">o</span><span class="&3">o</span><span class="&6">l</span>
    <span class="&~0 &b">black background</span>
    </pre>
        </div>
    </div>

Text can also be bold, strikethrough, underline, italic or removed of formatting.

.. code-block:: python

    from wool import wprint
    wprint("&lBold &r&nUnderline&r &oItalics&r &mStrikethrough")


.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre class="&f"><span class="&l">Bold </span><span class="&n">Underline</span><span class="&o"> Italics </span><span class="&m">Strikethrough</span></pre>
        </div>
    </div>


Terminals support a wide range of colors which are not covered by the base format codes. Wool can use hex codes to display a specific color as well.

.. code-block:: python

    from wool import wprint
    wprint("use &[#1793d1]ars&r")


.. raw:: html

    <div class="notranslate">
        <div class="highlight">
        <pre id="data-highlight" class="&f">use <span color="#1793d1">ars</span></pre>
        </div>
    </div>



