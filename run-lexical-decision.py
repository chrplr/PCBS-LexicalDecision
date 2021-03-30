#! /usr/bin/env python
# Time-stamp: <2021-03-30 15:49:50 christophe@pallier.org>
# This code is distributed under the GNU GENERAL PUBLIC LICENSE version 3
""" Lexical decision experiment.

The experiment consists in a series of trials, described in `resources/trials.csv`.

In each trial, a letter string stimulus is displayed a the center of the screen. The participant must press a button as quickly as possible to indicate if it is word or not.
"""

import sys
import random
import pandas
from expyriment import design, control, stimuli, misc


WORD_RESPONSE_KEY = misc.constants.K_j
NONWORD_RESPONSE_KEY = misc.constants.K_f
NONWORD_CATEGORY = "PSEUDO"
INTER_TRIAL_INTERVAL = 1500  # delay between two trials
MAX_RESPONSE_TIME = 2500  # deadline for response time (msec)
AUDIO_FEEDBACK_FILE_PATH = 'resources/wrong-answer.ogg'

USAGE = """Usage: run-lexical-decision.py FILE

Argument:
  FILE     :  a csv file with three columns: 'Category', 'Frequency', 'Item'.

Runs a lexical decision experiment presenting the items on by one.
"""

INSTRUCTIONS = """You will see a sequence of written stimuli.

    When you recognize an existing word, press the 'J' key; otherwise press the 'F' key .

    Try to be as quick as possible (your reaction tims is being measured)...

    ... but without making too many mistakes (a buzzer sound will be played for wrong answers)

    Now, place your index fingers on the keys 'F' (Non-word) and 'J' (Word).

    And press the SPACE BAR to start (To abort the experiment, press ESCAPE).
"""

#######################################################################

if len(sys.argv) < 2:
    print(USAGE)
    sys.exit()
else:
    # read a file describing the stimuli
    trial_stims = pandas.read_csv(sys.argv[1])

    # Check that the file contains the necessary columns
    assert all([colname in trial_stims.columns for colname in ['Category', 'Frequency', 'Item']])

    # randomize the rows of trial_stims so that the stimuli are presented in a random order
    trial_stims = trial_stims.sample(frac=1).reset_index(drop=True)


#######################################################################
# Prepare the experiment
exp = design.Experiment(name="Lexical Decision Task", text_size=40)


control.initialize(exp)


exp.add_data_variable_names(list(trial_stims.columns) + ['response_key', 'rt', 'is_correct'])

negative_feedback = stimuli.Audio(AUDIO_FEEDBACK_FILE_PATH)

###########################################################################
# Run the experiment
control.start(skip_ready_screen=True)

stimuli.TextScreen("Instructions", INSTRUCTIONS).present()
exp.keyboard.wait_char(' ')

for _, t in trial_stims.iterrows():
    exp.screen.clear()
    exp.screen.update()

    stim = stimuli.TextLine(t.Item)
    exp.clock.wait(INTER_TRIAL_INTERVAL - stim.preload())
    stim.present()

    button, rt = exp.keyboard.wait([WORD_RESPONSE_KEY, NONWORD_RESPONSE_KEY],
                                   duration=MAX_RESPONSE_TIME)

    is_correct = ((button == NONWORD_RESPONSE_KEY) and (t.Category == NONWORD_CATEGORY)) or  \
                 ((button == WORD_RESPONSE_KEY) and (t.Category != NONWORD_CATEGORY))

    if not is_correct:
        negative_feedback.play()

    exp.data.add([t.Category, t.Frequency, t.Item, button, rt, is_correct])

control.end()
