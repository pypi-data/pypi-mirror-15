sonopod
=======

A simple command line podcast player for Sonos

why?
----

This little utilty is great for building a remote control for Sonos.

The primary use case is for a headless Raspberry pi, reading RFID cards
to choose podcasts to play on the Sonos speaker.

If you find any other use for it, add your story!

examples
--------

help text
~~~~~~~~~

.. code:: bash

    $ ./sonopod.py --help
    SonoPod is a command line client to feed your Sonos with podcasts
    Copyright 2016 <havard@gulldahl.no>, GPLv3 licensed
    Usage: sonopod [-h|--help] [--setsonos] [--volume NN] [podcast_url]
        [-h|--help]     This help text
        [--setsonos]    Set default Sonos speaker
        [--volume NN]   Set volume of default speaker to N, between 0 (silent) and 90 (max)
        [podcast_url]   Add a new podcast series to the library, and pick an episode to play

        If run without arguments, presents a list of podcasts in the library

set default Sonos speaker
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ ./sonopod.py --setsonos
    Choose a Sonos speaker
    [1]  Arbeidsrom
    [2]  Stue
    Set default>

set volume of default speaker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ ./sonopod.py --volume=21
    New volume of player is 21

add podcast series
~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ ./sonopod.py http://www.thenakedscientists.com/naked_scientists_podcast.xml
    Available episodes
    [1]  Cambridge Science Festival: Battle of the Brains
    [2]  The A - Zika of viruses: Preventing Pandemics
    [3]  Gravitational Waves: Discovery of the Decade?
    [4]  Could The Internet Die?
    [5]  Rules of Attraction: The Science of Sex
    Which episode to play>

listen to podcast from library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ ./sonopod.py
    Podcasts in library
    [1]  NRK – 200 år på 200 minutter
    [2]  NRK – Einstein – på sporet av den tøyde tid
    [3]  Everyday Einstein's Quick and Dirty Tips for Making Sense of Science
    [4]  NRK – Nyhetsmorgen
    [5]  Freakonomics Radio
    [6]  Valebrokk og Co.
    [7]  NRK – Ekko - et aktuelt samfunnsprogram
    [8]  NRK – Ytring
    Choose podcast> 6
    Available episodes
    [1]  Her bor fremtidens boligvinnere
    [2]  Må vaskehjelpen subsidieres for å få kvinner i full jobb?
    [3]  Lakselus til tross, vi har så vidt sett starten på lakseeventyret
    [4]  Økonomisk toppmøte: Èn ting er mer verdt enn oljen
    [5]  Hvor ille kan oljebremsen bli? Vi har spurt industritoppene før sentralbanksjefens årstale
    Which episode to play> 2

ChangeLog
---------

0.1.2 (2016-06-03)
~~~~~~~~~~~~~~~~~~

- Add ``--volume=XX`` option to set volume on default speaker.

0.1.1 (2016-03-20)
~~~~~~~~~~~~~~~~~~

-  Tool is installed as ``sonopod.py`` in your path
-  Add code to choose Sonos speaker if you have more than one. Run with
   ``--setsonos`` to set speaker.
-  Add command line option ``--help``
-  Don't depend on the ``builtin`` module

0.1 (Unreleased)
~~~~~~~~~~~~~~~~

-  Working proof of concept

