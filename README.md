# Wordle Word Generator
Just a simple little python script to tell you what words match the current board state.

## Installation
Clone the repo, install python3 and install dependencies with `pip install -r requirements.txt`

## Useage
I made this when I got stuck on "aroma". My programming skills are marginally better than my word guessing skills.
To use this for your own board state, instantiate a new Word with the current letters (anything other than a letter
will be interpreted as a wildcard), removing any already-guessed letters from a specific letter (if you've gotten a
yellow letter for a particular box), and then running the thing. Running word.printOptions() will run the logic
and print the results kinda nicely. If you just need the words in a list, call word.findOptions().

Running twice (why would you run twice? idk, but you do you) isn't cached or anything; it'll filter for repeats,
but that's it.

For more details and an example of how to set up and run, check out the `if __name__ == '__main__'` function, in
wordgen.py.