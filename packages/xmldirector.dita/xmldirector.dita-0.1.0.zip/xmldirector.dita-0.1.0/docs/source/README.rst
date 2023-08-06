xmldirector.dita
================

DITA conversion support for XML Director

This module packages the 

- DITA Open Toolkit
- XMLMind DITA Converter

as Python module.

API
---

The module provides the following API::

    result = xmldirector.dita.converter.dita2html(ditamap, output_dir_or_file, converter)


- ``ditamap`` - path to DITA map file
- ``output_dir_or_file`` - output directory (DITA) or output filename (DITAC)
- ``converter`` - name of the converter to be used (``dita`` for DITA OT or ``ditac`` for 
   XMLMind Dita converter)


    output_filename = xmldirector.dita.html2dita.html2dita(html_filename, infotype, output_filename)

- ``html_filename`` - name of HTML input file
- ``output_filename`` - name of generated DITA file (a temporary file will be generated if omitted)
- ``infotype`` - DITA content type (topic, task, reference, concept)

Commandline usage
-----------------

You can start a DITA conversion from the commandline::

  > bin/dita2html -d some.ditamap -o output_directory -c dita|ditac

- ``-d`` - path to DITA map file
- ``-o`` - name of output directory (for DITA-OT) or the HTML output file
  (XMLMind DITAC)
- ``-c`` - name of the converter to be used (``dita`` for DITA OT or ``ditac`` for 
   XMLMind Dita converter)


You can convert a HTML file to DITA through the commandline::

    bin/html2dita -h
    usage: html2dita [-h] [-i HTML_FILENAME] [-f topic] [-o None]

    optional arguments:
      -h, --help            show this help message and exit
      -i HTML_FILENAME, --html-filename HTML_FILENAME
                            Input HTML filename
      -f topic, --infotype topic
                            DITA type (topic, concept, reference, task)
      -o None, --output-filename None
                            Output DITA filename
      


License
-------
This package is published under the GNU Public License V2 (GPL 2)

Source code
-----------
See https://github.com/xml-director/xmldirector.dita

Bugtracker
----------
See https://github.com/xml-director/xmldirector.dita/issues


Author
------
| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com

