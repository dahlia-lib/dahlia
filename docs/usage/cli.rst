Dahlia CLI
========

Dahlia can be used via its CLI to provide formatting.
It is invoked using ``dahlia``.


To see that Dahlia is installed correctly and working, run the test command.
This shows all the formatting codes and their resulting formatting.

.. code-block:: bash

    $ dahlia --test

.. raw:: html

    <div class="highlight-bash notranslate">
        <div class="highlight">
            <pre><span class="&0">0</span><span class="&1">1</span><span class="&2">2</span><span class="&3">3</span><span class="&4">4</span><span class="&5">5</span><span class="&6">6</span><span class="&7">7</span><span class="&8">8</span><span class="&9">9</span><span class="&a">a</span><span class="&b">b</span><span class="&c">c</span><span class="&d">d</span><span class="&e">e</span><span class="&f">f</span><span class="&g">g</span><span class="&l &f">l</span><span class="&m &f">m</span><span class="&n &f">n</span><span class="&o &f">o</span></pre>
        </div>
    </div>



Basic Use
---------

Just like programmatic Dahlia, the CLI uses the same methods of formatting.
The primary argument is the text to be formatted.

.. code-block:: bash

    $ dahlia "&aw&co&3o&~0&6l"

.. raw:: html

    <div class="highlight-bash notranslate">
        <div class="highlight">
            <pre><span class="&a">w</span><span class="&c">o</span><span class="&3">o</span><span class="&~0 &6">l</span></pre>
        </div>
    </div>

Optional Arguments
------------------

Depth
_____

``--depth``/``-d`` sets the depth of the colors to output. Options are ``3``, ``8`` and ``24`` with each corresponding their respective bit colors. 
See :ref:`Format Reference <formatref>` for what the depths correspond to.

.. code-block:: bash

    $ dahlia "&~0&624&7-&abit" --depth 24
    
.. raw:: html

    <div class="highlight-bash notranslate">
        <div class="highlight">
            <pre><span class="&~0"><span class="&6">24</span><span class="&7">-</span><span class="&a">bit</span></span></pre>
        </div>
    </div>

Clean
_____
``--clean``/``-c`` removes all Dahlia formatting sequences from a string.

.. code-block:: bash

    $ dahlia -c "&aw&co&3o&~0&6l"
    dahlia


