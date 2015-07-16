Champions with fastest wins for each player
===========================================

Requirements
------------

* Can make use of featured game players
* Doesn't need summoner endpoint
    * Can pull in some data anyway e.g. summoner level, current masteries, etc
* Will make use of stats (e.g. max time played, total games played)

Problems
--------

* Not super interesting
* Scope maybe too limited


Best builds based on wins with individual or combinations of items
==================================================================

Requirements
------------

* Can indirectly make use of featured game players
* Doesn't need summoner endpoint
* Will make use of stats

Problems
--------

* Requires match history which doesn't span far back, might be tricky without aggregation over time
* Not sure how meaningful it would be
* Tricky to segment into different champions, positions & roles


Creep scores correlated with win rate (per champion / top win rate champions?)
==============================================================================

Requirements
------------

* Can make use of featured game players
* Doesn't need summoner endpoint
* Will make use of stats

Problems
--------

* Not very interesting - outcome is probably obvious i.e. higher the better
* Scope maybe too limited


Detect cheaters based on match history
======================================

Monitor the following on a per champion basis for each summoner:
    - Continuous godly scores (super high cs, few deaths, high kills, etc) (potential scripting)
    - Abrupt change from bad average scores / cs to godlike scores / cs (different player / began scripting)
    - Many poor scores that result in high win rates (potential drop hack)
    - Playing non-stop for days / without breaks (potential bot)

Requirements
------------

* Can make use of featured game players
* Doesn't need summoner endpoint
* Will make use of stats

Problems
--------

* Might not work
* Requires match history
* Probably too much work


Team builder tool 
=================

Provide your summoner ID or team ID and try and match with other players that might fit based on:

* Timezone
* Language
* Skill level
* Roles plated
* Champion pool

Requirements
------------

* Doesn't make use of featured game players
* Will need summoner endpoint
* Will make use of stats

Problems
--------

* Probably too much work
* Would require lots of data analysis


Player stats
============

Stats pages for all players in a region including:

* Most kills in a match ever
* Highest cs by 20min ever
* Most time played
* Etc

Requirements
------------

* Doesn't make use of featured game players
* Will need summoner endpoint
* Will make use of stats

Problems
--------

* Probably too much work
* Would require lots of data analysis
* One of the more obvious solutions to the test

Current best players based on champion
======================================

* Per game
* Per all playing featured players

Requirements
------------

* Can make use of featured game players
* Might not need summoner endpoint
* Will make use of stats

Problems
--------

* Maybe not that interesting


Dream team from featured matches
================================

Look at all players in all currently featured matches and propose various dream teams:

* Based purely on positions + win %age
* based on positions + current champ + win %age
    * With champion synergy
* Based on player traits
    * Aggressive / defensive / team oriented / ...
        
Requirements
------------

* Can make use of featured game players
* Will need summoner endpoint
* Will make use of stats

Problems
--------

* No obvious problems


Achievements system for featured players
========================================

Most aggressive, snowball, preferred position, etc

Requirements
------------

* Can make use of featured game players
* Will need summoner endpoint
* Will make use of stats

Problems
--------

* Maybe not super interesting
* Another obvious solution to the test


Odds of teams winning - CHOSEN IDEA
===================================

* Simple version:
    * Calculate win %age average for both teams
    * Normalize it to rounded relative percentages between the teams (XWin% / RedWin% + PurpleWin% * 100)
    * Calculate the GCD of each win %age (from fractions import gcd; gcd(p1, p2))
    * Divide each value by the GCD to get the odds
    
* More complex version:
    * Factor in champion win rates
    
* Even more complex version:
    * Factor in players current form on each champion
    
* Track how accurate the system is over time based on game outcomes
    * Plot graph
    
* Profile page for each player breaking down individual stats
    * Current form
    * Win rate with champion
    * More?
    
Requirements
------------

* Can make use of featured game players
* Will need summoner endpoint
* Will make use of stats

Problems
--------

* No obvious problems