Overview of Application
=======================

* TOWRITE

Key Technological, Architectural, Design & Implementation Decisions
===================================================================

Python Flask Web Server
-----------------------

* Simple Python server using Flask for the routing

Templating & Data Presentation
------------------------------

* Jinja2 templates for rendering, possibly with some data injection
* Front end markup using HTML5 & Sass
* Hopefully minimal Javascript, limited to JQuery and potentially D3; this is the main motivation for not using a framework to avoid bloat
* Front-end will AJAX from the various end points it cares about

Build Process
-------------

* Built using gulp

MySQL & SQLAlchemy
------------------

* MySQL database for simplicity

* The database was a real pain to setup. I chose to use Flask-SQLAlchemy which I hadn't used much before, and in hindsight 
that was probably not a good idea. The documentation is pretty limited and it turns out there's some fairly serious bugs. 
The main pain point was caused by Flask-SQLAlchemy not to supporting "Associated" tables, i.e. many to many join 
tables that can also have attributes. In the end I refactored my database which removed this problem anyway. On the 
plus side I learnt a lot and now know most of the common pitfalls!

Daemon & LoL API
----------------

* TOWRITE

Rationale for Choosing Game Odds Idea (see ideas.md for other ideas)
====================================================================

* No obvious problems in terms of hitting the test requirements or being doable in the time frame
* Plenty of scope for additional features, time permitting
* I think it's interesting
* I already took too long deciding and need to pick something, let's do it! :)

What I Would Change With More Time
==================================

The following are a list of additional features, architectural changes and refactorings that 
I would have liked to have done given more time. In no particular order:

Odds Calculations
-----------------

* TOWRITE

Static Data & Images
--------------------

I am currently storing image urls (such as champion and summoner icon images) in the database against each summoner in each 
game. This isn't a great idea for a few reasons:
 
* The data will quickly become redundant once multiple games with the same champions and such are recorded.
* Images will require syncing in case they change. 
* URLs are harder to manipulate (e.g. if we want a different skin, pose, size etc).

A more robust solution is required for static data in general. This might not be so easy in terms of caching, as we don't 
want to hit the LoL API every time we need an image, but we also want to ensure the images are up to date. This may require 
some database tables to store the data, and a daemon to check the Data Dragon version every so often to see if we need to 
update our cache.

API & Front End UI
------------------

An API should be created to expose the DB objects to the front end, and the front end modified to use AJAX to load 
the data. This would allow for the UI to update the odds and games in real time, as well as supporting asynchronous 
data processing of odds.

I didn't spend too much time refining the UI, although I think it came out OK if not a little basic. With 
more time I would have liked to make it a little prettier. I would also have considered using a front end web 
framework, such as AngularJS or React. This way I could get some nice widgets "for free", such as the ability to 
filter and sort the games in the UI. On the flip side I did make the UI reactive in terms of resizing images and 
other elements for different screen sizes, although this could definitely be improved - the mobile UI in particular 
probably needs some structural changes.

Not all the data recorded by the daemon is currently exposed on the UI. I had initially intended to include a profile 
page for each summoner, showing more information about the different champions that have played in ranked games, their 
profile icons, summoner level and more. Some other data is also exposed in a "raw" way, for example the game queue 
types, which should have been mapped to a friendly name.

Task Queue & Processing
-----------------------

* Using a proper task queue when loading data like e.g. Celery with RabbitMQ.

Logging & Debugging
-------------------

* I didn't add a logger, this should definitely be added.

Integration & Smoke Tests
-------------------------

* Integration tests!!!

* Smoke tests to test the API during network outages etc. I found a lot of edge cases here just through testing (since 
my internet at home is pretty dodgy!).

Supervisor
----------

* TOWRITE

Extras with Time
================


* Improve the UI
* Add additional features
* Make the data endpoints properly REST
* Launch and manage the daemon properly with supervisord
* Consider adding a front end framework (Angular or React)
* Create a proper deployment strategy (this is supposed to be production ready after all)
* Support multiple country platforms / zones
* Random background champion image
* Live game odds based on current scores and such
* Game odds based on specific champion win rates
* Show game mode
* UI ordering and filtering
* Summoner profile pages
* Tracking of prediction rates over time
* Tracking of game outcomes
* Responsive image sizes
* Daemon health check endpoint
* Fix problem updating existing summoner (bug happened when adding new champion stats for existing summoner)
* Make game queue a readable name, not id
* Further attempt to fix the SQLAlchemy association table