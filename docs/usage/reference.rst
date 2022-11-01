Reference
=========

.. _formatref:


Color Format Codes
------------------

Each digit/letter corresponds to a hex value (dependent on the color depth).
The coloring can be applied to the background if a ``~`` is inserted between ``&`` and the code.

.. list-table:: 
    :header-rows: 1
    :class: format-code

    * - Code
      - 3-bit
      - 4-bit
      - 8-bit
      - 24-bit
    * - ``0``
      - #000000
      - #000000
      - #000000
      - #000000
    * - ``1``
      - #000080
      - #000080
      - #0000af
      - #0000aa
    * - ``2``
      - #008000
      - #008000
      - #00af00
      - #00aa00
    * - ``3``
      - #008080
      - #008080
      - #00afaf
      - #00aaaa
    * - ``4``
      - #800000
      - #800000
      - #af0000
      - #aa0000
    * - ``5``
      - #800080
      - #800080
      - #af00af
      - #aa00aa
    * - ``6``
      - #808000
      - #808000
      - #ffaf00
      - #ffaa00
    * - ``7``
      - #c0c0c0
      - #c0c0c0
      - #a8a8a8
      - #aaaaaa
    * - ``8``
      - #000000
      - #aaaaaa
      - #585858
      - #555555
    * - ``9``
      - #000080
      - #0000ff
      - #afafff 
      - #5555ff
    * - ``a``
      - #008000
      - #00ff00
      - #5fff5f
      - #55ff55
    * - ``b``
      - #000080
      - #00ffff
      - #5fffff
      - #55ffff
    * - ``c``
      - #800000
      - #ff0000
      - #ff5f5f
      - #ff5555
    * - ``d``
      - #800080
      - #ff00ff
      - #ff5fff
      - #ff55ff
    * - ``e``
      - #808000
      - #ffff00
      - #ffff5f
      - #ffff55
    * - ``f``
      - #c0c0c0
      - #ffffff
      - #ffffff
      - #ffffff
    * - ``g``
      - #808000
      - #808000
      - #d7d700
      - #ddd605

Formatting Codes
----------------

.. list-table::
    :header-rows: 1
    
    * - Code
      - Result
    * - ``l``
      - Bold
    * - ``m``
      - Strikethrough
    * - ``n``
      - Underline
    * - ``o``
      - Italic
    * - ``r``
      - Reset formatting

Custom Colors
-------------

For colors by hex code, use square brackets containing the hex code inside of it.


.. list-table::
    
    * - Foreground
      - ``&[#XXXXXX]``
    * - Background
      - ``&~[#XXXXXX]``

``X`` represents the hex value of the color.
