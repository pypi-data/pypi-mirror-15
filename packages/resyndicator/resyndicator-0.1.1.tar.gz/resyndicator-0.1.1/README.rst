============
Resyndicator
============

Purpose
-------

Imagine the Resyndicator as a thing that does stuff.

Specifically, it aggregates data from various sources into Atom feeds. If you have a list of a couple hundred data sources, such as feeds and Twitter users, and want to share the aggregate of those entries or updates between your various devices (computers, phones, etc.), your colleagues, or even the visitors of your website, then that’s just what I wrote the Resyndicator for.

If you’ve always used the Resyndicator to aggregate your feeds, moving away from Google Reader is peanuts, since you’ve always kept your data on your own server and only delivered an aggragated copy to Google.

Setup
-----

I couldn’t find a decent Atom generator library, so I used the one from Django and `refactored it until hardly a line from the original was left`__. I think I’ll make it a separate Atom-only library, since I don’t care for RSS.

__ https://github.com/Telofy/feedgenerator

Then there is also Utilofies__, which I’ll start using at some point.

__ https://bitbucket.org/Telofy/utilofies

If you are using mr.developer, you can include them in your Buildout config just as I did in the buildout.cfg of this framework.

::

    [sources]
    feedgenerator = git https://github.com/Telofy/feedgenerator.git
    utilofies = git https://bitbucket.org/Telofy/utilofies.git

You can pull in the Resyndicator itself the same way.

For the readability content extraction, you’ll also need a few dependencies of lxml::

    sudo aptitude install libxml2-dev libxslt-dev

To run the tests, you’ll need pyVows, which requires libevent-dev. Unfortunately, it doesn’t seem to work at the moment; got to figure out why at some point.

::

    AttributeError: ResourceManager instance has no attribute '_warn_unsafe_extraction'

To run the various services, I recommend Supervisor.

Usage
-----

The structure is similar to that of frameworks like Django. Just have a look at the vows/ directory. There you’ll find a ``settings.py`` and a ``resources.py``. The ``settings.py`` contains miscellaneous settings such as your database URI and the base URI from which the aggregate feeds are to be served. The ``resources.py`` contains all the cool stuff.

In the ``resources.py`` you define the data sources—feeds or streams such as Twitter—and the resyndicators. For each resyndicator, you define a query and a title which will determine its ID and thus its identity. If you change the title you create a different feed. The query determine the entries of the feed and are written are SQLAlchemy where statements.

You can then start the cyclic fetcher with ``bin/resyndicator -s mypackage.settings daemon --fetcher``, the streams with ``bin/resyndicator -s mypackage.settings daemon --stream 0``, and the server with ``bin/resyndicator -s mypackage.settings server`` unless your Buildout is configured some weird way.

Tiny Tiny RSS
-------------

It’s pretty cool. I used it for about half a year, though I had to hack it a bit (not fun, for not Python) to support update intervals of one minute and longer feed URLs. Finally I needed to specify developer keys in the HTTP headers, retrieve feeds through proxies, and make them all push-enabled. I had to move away from Tiny Tiny RSS. It does have a lot of features, however, that I never really needed—and which won’t find their way into the Resyndicator—such as the web interface.

Update: Now that Google Reader is gone, I’m using Tiny Tiny RSS as frontend for the Resyndicator. NewsBlur, unfortunately, `cuts the feeds off after a small number of recent items`__; I could never read them as fast as it discards them.

__ https://getsatisfaction.com/newsblur/topics/feed_cut_off_after_100_entries
