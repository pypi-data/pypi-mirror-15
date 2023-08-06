lahman-chitown-fix
==================

Fixes a persistent error in the Lahman 2014 baseball database.  
The last eight fields in the 'teams' table are mixed up between the two Chicago teams.
This fixes the database.

First release.  Only tested with python 2.7.11

If not installed and you want to run manually simply alter the main() and remove references to 'login_dict' and replace login details where 'mydb' is declared.
