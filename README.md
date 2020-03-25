# LangEvolve

_author_: **ojima**

A conlanging program to apply sound change rules on words or text.

## Installation

### Prerequisites

To run LangEvolve, you will need to have python 3 installed, along with the `gi` package. To install python, please refer to the [python website](https://www.python.org/). To install `gi`, you can refer to the [gi manual](https://pygobject.readthedocs.io/en/latest/getting_started.html).

I will see if I can create compiled binaries for Windows at a later stage.

### Installation

#### Cloning the repo

Clone the repository using `git` and run using your preferred python executable.

```
	git clone https://github.com/ceronyon/LangEvolve
	cd LangEvolve
	python src/main.py
```

## Usage

When booting `LangEvolve`, you are met with a screen with three text boxes and an output field. The leftmost text box is the input lexicon, the center ones are for the categories and the rules.

If this is your first time, hit the `import rules` button and select the attached `portuguese.json` file, then do the same for `import words` and select the `latin.txt` file. You will see a bunch of Latin words pop up on the left, with a lot of complicated characters in the center. When you hit `apply rules`, you should see the box on the right display the Latin words evolved to Portuguese according to the rules in the center box.

### Rules

`LangEvolve` uses **regex** (regular expressions) to parse its rules. In the rule input box, you can give a series of rules of the format `input>output` (one per line). When you click the `apply rules` button, `LangEvolve` will apply each rule in order from top to bottom to each word and change it accordingly. For example, the rule `n>m` will replace every instance of the letter _n_ with the letter _m_.

Using **regular expressions** allows for more complicated changes. For example, the rule `[sm]$>` will hit _either_ the letters _s_ or _m_ (as denoted by `[sm]`) but _only_ if they are at the end of a word (as denoted by `$`), and remove them from the string. We see this in the example where _focus > fogo_, and the final _s_ drops.

### Categories

A category is a set of characters defined for shorthand notation in the rules entry. Whenever you click the `apply rules` button, `LangEvolve` will build its list of rules based on the input rules, substituting user-defined categories where needed. While it is building its list, however, `LangEvolve` will check whether rules contain the symbol `%` and substitute in categories accordingly. Categories are expected to consist of a single alphabetical character (case-sensitive). For example, if a rule contains `%Vr` it will check for the category defined `V` and substitute that in before the letter `r`.

Substitutions follow two rules: 

- If a `%` symbol is found in the output, it will check to see if a category is present in the input as well - both the input and output need to have a single category containing the same amount of symbols. The program will zip over the two categories and create a rule for each pair of entries. _Example:_ in the Portuguese list, the rule `%L>%V` will make the program search for the categories named `L` and `V`, which in this case refer to long and short vowels respectively. It will accordingly create the rules `ā>a`,`ē>e`,`ī>i`,`ō>o` and `ū>u`. The program will give an error if either side of the rule contains not exactly one category, or if the two categories are of unequal length.

- If a `%` symbol is found only in the input, then the program will replace that symbol by the string defined as that category, encapsulated by square brackets. This means that the rule will match for any character present in the category. _Example:_ in the Portuguese list, the rule `(%C)er(%V)>\1r\2` will be turned into `([ptcqbdgmnlrhs])er([aeiou])>\1r\2`, meaning that any letter _e_ that follows a consonant from the list `C` and preceding and _r_ and a vowel will drop.

## Planned Features

Below is a non-exhaustive list of features possibly planned for the future. Depending on how much this program gains traction, I may or may not continue working on it.

- Be more flexible/extensive in category parsing. For example, allow for rules which contain multiple categories in the input/output, e.g. `(%V)%S(%V)>\1%Z\2`. May need to change the formatting of rules to something like `(%V%)%S1%(%V%)>\1%Z1%\2`, with two symbols per variable name, to further encapsulate numerical characters for parameter referencing.

- Allow for better input/output saving.

- Creation of language families.

    - Mass-evolution along all branches of a family.
    
    - Comparative linguistic tools, such as visualizing lexicon relations for individual words, calculating (Levenshtein) evolutionary distance on lexicon scale, etc.

## Using this Program

Feel free to use this program, suggest changes to it, etc. however you want. If you use this program as a base for your own code, branch off of it or in any other way build software based on the contents of this repo, please give credit to the original author, ojima.