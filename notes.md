Overview of Approach
====================

* Simple Python server using Flask for the routing
* Jinja2 templates for rendering, possibly with some data injection
* Front end markup using HTML5 & Sass
* Hopefully minimal Javascript, limited to JQuery and potentially D3; this is the main motivation for not using a framework to avoid bloat
* Built using gulp
* MySQL database for simplicity
* Probably going to use Celery to run API data ingestion tasks - this might be overkill
* Front-end will AJAX from the various end points it cares about

Rationale for Choosing Game Odds Idea (see ideas.md for other ideas)
====================================================================

* No obvious problems in terms of hitting the test requirements or being doable in the time frame
* Plenty of scope for additional features, time permitting
* I think it's interesting
* I already took too long deciding and need to pick something, let's do it! :)

What I Would Change With More Time
==================================

* Storing image urls (such as champion and summoner icon images) in the database isn't a great idea since they then 
require syncing in case they change. It also makes it much harder to manipulate (e.g. if we want a different skin, pose, 
size etc). They should be loaded (and cached) from the API. I did this just to save time.

* Using a proper task queue when loading data like e.g. Celery with RabbitMQ.

* The whole loading of games, summoners and champion stats should probably be done in a transaction that is only 
committed if everything loads successfully. I guess we'll see how this goes. 

* I didn't add a logger, this should definitely be added.

* Integration tests!!!

* The database was a real pain to setup. I chose to use Flask-SQLAlchemy which I hadn't used before, and in hindsight 
that was probably not a good idea. The documentation is pretty limited and it turns out there's some fairly serious bugs. 
The main pain point was caused by Flask-SQLAlchemy not to supporting "Associated" tables, i.e. many to many join 
tables that can also have attributes. This forced me to move the "team_id" and "champion_id" fields to the summoners
table as a hack just to get the project working. It also seems to have some funny caching going on.

TODO List
=========

~1. Implement the woeful amount of unwritten unit tests
2. Write up notes
3. Check readme details are correct
4. Ensure setup.py works

Extras with Time
================

* Create endpoints to expose the DB objects
* Add front end AJAX calls to the endpoints
* Add proper API rate limit handling
* Use Celery for a task queue when ingesting API data
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
* Don't allow partial games to be displayed (this shouldn't happen but it is, SQLALchemy strikes again)
* Front end should emulate the database, but instead it's getting cached from the moment it launches (again thanks SQLAlchemy)
* Make game queue a readable name, not id

* Fix this - looks like network problem - should retry after a delay:
	api url: https://euw.api.pvp.net/api/lol/euw/v1.4/summoner/by-name/helvis?api_key=db60a3be-abf0-479e-b99f-99515a164e55&
	Failed to get API data: <urlopen error [Errno 8] nodename nor servname provided, or not known>