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

* TODO


TODO List
=========

1. Pick an idea for what the app will actually do
2. Create DB objects required for this idea
3. Create endpoints to expose the DB objects
4. Add front end AJAX calls to the endpoints
5. Create logic layer transforming the data into our idea
6. Display the data logically on the front end
7. Create simple daemon to continually check for updated feature games
8. Implement tasks to convert API data to DB objects
9. Write up notes
10. Check readme details are correct
11. Ensure setup.py works

Extras with Time
================

* Add proper API rate limit handling
* Use Celery for a task queue when ingesting API data
* Improve the UI
* Add additional features
* Make the data endpoints properly REST
* Launch and manage the daemon properly with supervisord
* Consider adding a front end framework (Angular or React)
* Create a proper deployment strategy (this is supposed to be production ready after all)
