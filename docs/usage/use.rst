Using wool to format text
=========================


Wool CLI
--------

Wool can be used via its CLI to provide formatting.
It is invoked using ``wool``.


To see that wool is installed correctly and working, run the test command.

.. code-block:: bash

    $ wool --test

Output:

.. raw:: html

    <div class="highlight-bash notranslate">
        <div class="highlight">
            <pre><span class="&0">0</span><span class="&1">1</span><span class="&2">2</span><span class="&3">3</span><span class="&4">4</span><span class="&5">5</span><span class="&6">6</span><span class="&7">7</span><span class="&8">8</span><span class="&9">9</span><span class="&a">a</span><span class="&b">b</span><span class="&c">c</span><span class="&d">d</span><span class="&e">e</span><span class="&f">f</span><span class="&g">g</span><span class="&l &f">l</span><span class="&m &f">m</span><span class="&n &f">n</span><span class="&o &f">o</span></pre>
        </div>
    </div>
    

Programmatic Wool
-----------------

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



