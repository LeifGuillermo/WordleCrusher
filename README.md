# Application Usage

## Scripts

There are two main scripts you can run as a user:

* **wordle_crusher.py**
* **game_clone.py**
  <br>Both of these scripts run the **main.py** files in the respectively-named packages **wordle_crusher** and **game_clone**.

The **game_clone** package is pretty straight-forward. The game exists in one file.*
<br>* **_(subject to change. Hopefully I'll remember to update this README if it does.)_**

The **wordle_crusher** package's main method is in `main()`, as expected, but there are quite a few dependencies on the
other
<br>files in the package as well.

### Script Arguments:

#### wordle_crusher

**Example:**<br>
``python wordle_crusher.py -a -i arosfidwycb -m ____e,__le_,_etl_ -c _lent``

The explanations below make use of the term "guess". A guess is always 5 characters wrong, where characters that are not
<br>known are represented by underscores, `_`

This example uses:
<br>

* `-a` to print all available words.<br>
* `-i` to list out all words that do not belong in the hidden word (found from previous guesses)
* `-m` guesses - each guess has underscores representing characters that do not belong in the hidden word, and the
  <br>characters are representative of characters that are misplaced. Guesses are separated with commas, and no spaces.
  <br>i.e. the first guess' `e` exists as the last letter in the guess, so words are then filtered so that e exists in
  <br>the words, but only if the words do not have e as the last letter.
* `-c` a single guess - in the example the letters `l` `e` `n` and `t` are in the correct positions, so the words are
  <br>filtered down to just words that have those specific characters in those specific positions.

## Unit Tests

The unit tests require pytest. To run them, simply run the command `pytest`on the command line from the project root
folder.

## TODOs:

* Make crusher application interactive (game_clone is already interactive) - this should just be a different script.
* I'd like to keep the existing functionality because it does work well still.
* Add 'suggested word ordering' since each available character exists in the available words, the words can be ordered
  <br>based on the rankings of the available characters in the words.
    * May want to make words with two or more of a character lower-ranking than words that do not have two or more of a
      <br>character since that is more useful in finding out which characters are available and which aren't.
* Update README usage for the game_clone
* Add more unit tests
* Consider looking into what can be object-oriented.
