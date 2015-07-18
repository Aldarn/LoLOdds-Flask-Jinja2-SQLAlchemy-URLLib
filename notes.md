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

* encoding issues

* network issues and unreliable responses

* rate limits

* modified timestamps

Odds Calculations
-----------------

Currently the odds are calculated by cumulating the total (and current champion) wins and losses for each team 
for each game:

	all team summoners wins / all team summoners wins + all team summoners losses * 100

This gives us a percentage win rate for each team. We can then normalise these against each other to get the 
win chance relative to the opposing team:

	blue team win chance: blue team win rate / blue team win rate + purple team win rate * 100
	purple team win chance: purple team win rate / blue team win rate + purple team win rate * 100
	
With these two values we can calculate the greatest common divisor to reduce the chances to a ratio. In order 
for this to work effectively, percentages are rounded to the nearest percent. This has the caveat of losing some 
accuracy, as well as not supporting more extreme odds in cases of odds > 100 : 1, however I don't expect this 
to happen given the matchmaking algorithm that matches teams in the first place.


Rationale for Choosing Game Odds Idea (see ideas.md for other ideas)
====================================================================

* No obvious problems in terms of hitting the test requirements or being doable in the time frame
* Plenty of scope for additional features, time permitting
* I think it's interesting
* I already took too long deciding and need to pick something, let's do it! :)


What I Would Change With More Time
==================================

The following are a list in no particular order of additional features, architectural changes and 
refactorings that I would have liked to have done given more time.

Odds Calculations
-----------------

As previously discussed, the odds are currently calculated on team win / loss total basis. However, it may be more 
meaningful to do this on a player by player basis using their individual win rates to get a team win rate average, i.e:

	(player1 wins / (player1 wins + player1 losses) + ... + playerN wins / (playerN wins + playerN losses)) * team size

Then the odds would be calculated by comparing both team's win rate averages. This would give more weight towards individual 
players, making weak and strong players have a greater skew of the odds.

In addition to this, there are many other metrics that I would have liked to included in the calculations:

* Summoner level
* Champion synergy
* Recent summoner form on the current champion
* Runes and masteries

Another really interesting feature I would like to add would be live game odds. This could be done by grabbing additional 
data relating to the current match from the API, such as:

* Total gold counts
* Distribution of gold to strongest summoners
* KDA ratios and their distributions
* Creep scores and their distributions
* Towers and inhibitors taken
* Build paths
* Power scaling of different champions

I'm sure there are more factors that could be included, and I think it would be fascinating to see the results.

Tracking of Predictions Over Time
---------------------------------

In addition to generating odds, I would love to add a feature that checks the outcome of games when they have ended 
and maps that back against the predicted odds. This could be rendered out in a graph using e.g. `D3.js`, showing 
how accurate the system has been over time.

League Platforms / Realms
-------------------------

The application was designed to work with platform EUW1, and some platform related config (e.g. API URLs) have 
been hard coded as such. This should be updated to support all platforms.

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

A REST API should be created to expose the DB objects to the front end, and the front end modified to use AJAX to load 
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

Although having a standalone daemon for interfacing with the LoL API has good performance benefits for the end user 
(since the data doesn't need to be loaded on demand), it could soon become a bottle neck with additional features or 
content from the API. 

This was the main rationale for designing the daemon as a pipeline of tasks to run on distinct domain objects. Extending 
this system to run asynchronously, using a distributed task queue such as `Celery` backed by a message broker such as 
`RabbitMQ`, would thus be relatively straight forward. This would dramatically improve the performance of the daemon 
and make it much more scalable.

It would also be useful to add a simple daemon health check endpoint, allowing the UI to communicate to the users when 
there are any issues with the game odds being processed.

Logging & Debugging
-------------------

I didn't add a logger, which should definitely be added. This wasn't really a huge problem during development since I 
still had output to the shell and unit tests, however it would make life easier especially to diagnose any problems 
that occur after deployment.

Integration & Smoke Tests
-------------------------

Currently there's a decent suite of unit tests which should have a high percentage of code coverage. Some of these unit 
tests are "integration test" like in that they use real data objects where possible and actually run and observe database 
operations on a test database.

That being said, a suite of end to end (user journey and key functionality) integration tests would add greater confidence 
to the system under more realistic conditions with real data.

Additionally, smoke tests to test the API during network outages and other disruptions would improve the robustness of 
the API daemon. I found a lot of edge cases here just through running the daemon whilst developing, due to random glitches 
on both ends of the wire.

Supervisor
----------

The daemon was designed to be managed using `supervisord`, a cron job / daemon process control system. This is how 
I was running it whilst developing, however I didn't get chance to commit my configuration in such a way that it 
would be setup automatically when installing the project. Since the daemon can also be ran manually simply by executing 
it directly with Python I didn't think it was worth spending time bundling this.

Deployment
----------

Currently there is no deployment strategy, although it should be possible to simply lift the build onto a server, 
install the requirements and start serving. 

A more appropriate approach would be to package the build into an egg (or similar depending on OS). This should be 
handled by various Jenkins jobs - for instance a build job, a job to deploy to staging and another to production.

Config is currently baked into the system via config files in the src/resources directory. This should be handled 
by a config management system e.g. Ansible, Puppet, Chef, etc.
