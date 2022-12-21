### Control Server
In order to run the server, change directory to the 
project's root directory, under the roo folder run:
##### python manage.py runserver

Migrations already run (following the instructions).


### Attack Bot
* The attack bot can be found under the attack_bot folder.
* At the moment, the address of the control server is static.
* Connectivity with the control server is based on polling 
mechanism (could and should be enhanced/upgraded to django channels).
* The bot is resilient for connectivity issues with the control server.
Obviously, resiliency is much wider area that I couldn't entirely cover under this assignment.
* The bot handles the attacks serially and can/should be enhanced to handle multiple attacks simultaneously  # bot-attack
