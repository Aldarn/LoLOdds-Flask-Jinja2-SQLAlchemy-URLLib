Overview of Application
=======================

I decided to implement a web application designed to continually calculate the odds of featured League of Legends 
games on EUW. These odds are based on both the overall win rates of the teams and the win rates of the teams 
based on the current champions being played. The games and their odds are then displayed on a web UI, with new 
featured games being continually added as they are exposed by the League of Legends API.

At a high level, the system consists of:

* A web UI for displaying games and odds
* A Python Flask server for rendering the pages and exposing the data
* A MySQL database for saving game data
* A wrapper around the LoL API for handling communications and data retrieval
* A daemon to continually poll the LoL API and update the database


Key Technological, Architectural, Design & Implementation Decisions
===================================================================

Python Flask Web Server
-----------------------

I decided to use Python Flask as a web application server. I chose this Framework as it is very lightweight, and I 
wasn't anticipating requiring a huge suite of functionality. It is also very simple to use and I have had prior experience 
and success using the technology. 

The Flask server is primarily responsible for routing and serving the relevant web application templates. 

Currently, the Flask server is also responsible for injecting the games and odds data into the templates. As will be 
discussed later, given more time I would have liked to have exposed this data via a REST API that the front end would 
interface with via AJAX.

Templating & Data Presentation
------------------------------

I decided to use the Jinja2 templating engine for rendering the web pages, as well as for displaying data injected 
from the server in a logical format. I chose this engine as it comes with direct integration with Flask, and I have also 
had prior experience and success using it.

The web pages themselves are written as purely HTML5 templates and Sass.

Build Process
-------------

The web application is built using gulp. In `gulpfile.js` there are various build steps that I have created in order to 
convert Sass to CSS, minify files and add sourcemaps, import bower dependencies, browserify includes and so forth. Once 
the application has been built the files are copied into the `build` folder. 

This process makes working on the front end very simple, as changes made to files are monitored by gulp and automatically 
rebuilt on the fly, allowing you to immediately see your changes in the browser. It also manages a lot of otherwise 
manual tasks automatically making development time much shorter.

MySQL & SQLAlchemy
------------------

I decided to use a MySQL database for saving game and summoner data from the LoL API. This was because of my familiarity 
with MySQL and the ease of which it is to setup. I didn't anticipate huge volumes of data or requests, and the data is 
inherently relational, so this seemed like a reasonable decision. 

I chose to use SQLAlchemy as an ORM in the hope of saving time by avoiding having to manually write DAOs (Data Access 
Objects) with raw SQL queries, along with mappers to convert to and from raw data to domain objects. Although I had 
a small amount of experience using SQLAlchemy before, this was mostly new to me. The decision was made mainly on 
recommendation from the community, and the fact that there is an extension, `Flask-SQLAlchemy`, designed to integrate 
Flash with SQLAlchemy.

In hindsight, choosing to use both SQLAlchemy and Flask-SQLAlchemy was probably not a good idea, given the test 
scenario and my inexperience with the technology. The documentation for Flask-SQLAlchemy is quite limited, and the 
syntax and usage also differs somewhat from pure SQLAlchemy. This meant I had to try and use the SQLAlchemy documentation 
and community to solve problems with the Flask-SQLAlchemy extension, which didn't necessarily translate 1 to 1. During 
this process I discovered some fairly serious bugs, the largest being the use of a "join table" between many to many 
relationships. At its simplest level, a table with just two keys, each a foreign key to other tables, solved this problem. 
However, I wanted to store some additional fields on this join table, which was not supported by Flask-SQLAlchemy. The 
online community suggested I convert my join table to an "associated" table, however this threw up a whole new set of 
problems. 

In the end I refactored my database which solved all of my problems, but overall this process was quite time consuming. 
On the plus side I have learnt a lot and now know most of the common pitfalls!

LoL API
-------

In order to interface with the League of Legends API, I created a base service responsible for building the API URLs, 
retrieving the data and handling any API response or network errors. I then wrote several wrappers around the API 
endpoints I was interested in (featured games, summoners by name, ranked stats and champion by id) providing methods 
accepting their relevant fields.

Communicating with the LoL API turned out to be more challenging than I had initially anticipated for a number of 
reasons. Firstly, the responses were unreliable: sometimes the API would be down or simply return empty data. Secondly, 
I discovered through network connection problems a whole new set of responses to handle, for instance no internet 
connection, gateway problems or SSL failures. Finally, I also ran into encoding problems for summoners with names 
making use of unicode characters.

Handling the first two problems was a case of adding exception handling for all the different possible API and network 
responses. In most cases I instructed the service to sleep for some time before reattempting the request. I also added 
handling for cases when the API request rate limit was exceeded.

Dealing with the encoding problem was slightly more difficult, especially with the unique way Python handles unicode. To 
solve these problems I implemented the following:

* Python files dealing with unicode were instructed to use UTF-8 encoding
* Summoner names had to be encoded as UTF-8, then when used in the summoner by name API endpoint had non-ASCII 
characters URL encoded
* Database fields had to be converted to use UTF-8 MB4 encoding and collation utf8mb4_unicode_ci

Daemon & Tasks
--------------

Rather than requesting data from the API on demand when a user connects to the web application, I decided it would be 
more efficient to have a separate daemon continually polling the API for new featured games, processing those and storing 
them in the database for the web application to serve directly. Although this may have been a premature optimization, 
I feel it was the right approach and actually processing a full game can take a fair amount of time which would have 
adversely effected the user experience if done on the fly.

The daemon was designed to be managed using `supervisord`, a cron job / daemon process control system, which I used 
during development. It is also possible to run it with Python directly.

Structurally, the daemon itself is a simple loop that respects the LoL API rate limits, sleeping for the recommended 
amount of time before polling for new data. The daemon then creates and runs tasks to process the received data. These 
tasks were designed to be modular and are responsible for transforming the received JSON to database objects. They 
handle both new data and updated data for existing objects. In the latter case the tasks make use of the various 
modified timestamps provided by the LoL API to determine whether the domain objects require updating or not. 

Although having a standalone daemon for interfacing with the LoL API has good performance benefits for the end user 
(since the data doesn't need to be loaded on demand), it could soon become a bottle neck with additional features or 
content from the API. 

This was the main rationale for designing the daemon as a pipeline of tasks to run on distinct domain objects. Extending 
this system to run asynchronously, using a distributed task queue such as `Celery` backed by a message broker such as 
`RabbitMQ`, would thus be relatively straight forward. This would dramatically improve the performance of the daemon 
and make it much more scalable. Since the overhead of designing and implementing the system as a series of tasks was 
minimal, I feel this was a good choice irrespective of whether a task queue is implemented. It also provided logical 
separation of concerns and decoupling.

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

Flask Server Calculations
-------------------------

Currently the Flask server is responsible for calculating the game odds. In hindsight, since these calculations are 
static once the game has been discovered, they could be a one time calculation ran as a task by the daemon. The daemon 
could then store the odds and percentages against the games and game summoners in the database. This would be much more 
efficient as currently they are calculated each time the page is requested. 

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

As previously discussed, to improve the performance of the daemon and task processing, an asynchronous task queue 
could be implemented using `Celery`.

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

As previously mentioned, I used `supervisord` to run the daemon whilst developing, however I didn't get chance to 
commit my configuration in such a way that it would be setup automatically when installing the project. Since the 
daemon can also be ran manually simply by executing it directly with Python I didn't think it was worth spending time 
bundling this.

Deployment
----------

Currently there is no deployment strategy, although it should be possible to simply lift the build onto a server, 
install the requirements and start serving. 

A more appropriate approach would be to package the build into an egg (or similar depending on OS). This should be 
handled by various Jenkins jobs - for instance a build job, a job to deploy to staging and another to production.

Config is currently baked into the system via config files in the src/resources directory. This should be handled 
by a config management system e.g. Ansible, Puppet, Chef, etc.
