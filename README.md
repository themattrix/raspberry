Raspberry
=========

This is a sandbox area for various Raspberry Pi projects. The only thing I've made so far is a tug-of-war
game.

Tug-of-War Game
---------------

    src/tugofwar.py

This is a simple tug-of-war style game between two opponents. Each player must press his button as rapidly
as possible to push the light toward the other player.

GPIO Pins in use:

    +----+----+----+----+----+----+----+----+----+----+----+----+----+
    |    |    |    |    |    | 15 | 13 | 11 |    |  7 |    |    |    |
    +----+----+----+----+----+----+----+----+----+----+----+----+----+
    |    |    |    |    | 18 | 16 |    | 12 |    |    |    |    |    |
    +----+----+----+----+----+----+----+----+----+----+----+----+----+

     7: Red LED
    11: Yellow LED
    12: Green LED
    13: Yellow LED
    15: Red LED
    16: Player 1 button
    18: Player 2 button

![alt text](https://github.com/themattrix/raspberry/raw/master/img/in_action.jpg "The game in action")