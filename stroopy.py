# -*- coding: utf-8 -*-

from psychopy import event, core, data, gui

from fileHandling import *


class Experiment:
    def __init__(self):
        self.stimuli_positions = [[-.2, 0], [.2, 0], [0, 0]]

    def create_window(self, color=(1, 1, 1)):
        # type: (object, object) -> object
        self.color = color
        self.win = visual.Window(monitor="testMonitor",
                                 color=self.color, fullscr=True)
        return self.win

    def settings(self):
        self.experiment_info = {'Subid': '', 'Age': '', 'Experiment Version': 0.1, 'Sex': ['Male', 'Female', 'Other'],
                                'Language': ['Swedish', 'English'], u'date': data.getDateStr(format="%Y-%m-%d_%H:%M")}
        self.infoDlg = gui.DlgFromDict(title='Stroop task',
                                       dictionary=self.experiment_info, fixed=['Experiment Version'])
        self.experiment_info[u'DataFile'] = u'Data' + os.path.sep + u'stroop.csv'
        if self.infoDlg.OK:
            return self.experiment_info
        else:
            core.quit()
            return 'Cancelled'

    def create_text_stimuli(self, text=None, pos=[0.0, 0.0], name='', color='Black'):
        '''Creates a text stimulus,
        self.text = text
        self.pos = pos
        self.name = name
        self.height = height
        self.color = color'''

        self.text = text
        self.pos = pos
        self.name = name
        self.color = color
        text_stimuli = visual.TextStim(win=self.win, ori=0, name=self.name,
                                       text=self.text, font=u'Arial',
                                       pos=self.pos,
                                       color=self.color, colorSpace=u'rgb')
        return text_stimuli

    def create_trials(self, trial_file, randomization='random'):
        '''Doc string'''
        self.trial_file = trial_file
        self.random = randomization
        self.data_types = ['Response', 'Accuracy', 'RT', 'Sub_id', 'Sex']
        with open(self.trial_file, 'r') as stimfile:
            self._stims = csv.DictReader(stimfile)
            self.trials = data.TrialHandler(list(self._stims), 1,
                                            method="random")

        [self.trials.data.addDataType(data_type) for data_type in self.data_types]

        return self.trials

    def present_stimuli(self, color, text, position, stim):
        self._stimulus = stim
        self.color = color
        self.position = position
        if self.experiment_info['Language'] == "Swedish":
            self.text = swedish_task(text)
        else:
            self.text = text
        self._stimulus.pos = position
        self._stimulus.setColor(self.color)
        self._stimulus.setText(self.text)
        return self._stimulus

    def running_experiment(self, trials, testtype):
        self._trials = trials
        self.testtype = testtype
        self.timer = core.Clock()
        stimuli = [self.create_text_stimuli(self.win) for _ in range(4)]

        for trial in self._trials:
            # Fixation cross
            fixation = self.present_stimuli('Black', '+', self.stimuli_positions[2], stimuli[3])
            fixation.draw()
            self.win.flip()
            core.wait(.6)
            self.timer.reset()

            # Target word
            target = self.present_stimuli(trial['colour'], trial['stimulus'], self.stimuli_positions[2], stimuli[0])
            target.draw()
            # alt1
            alt1 = self.present_stimuli(trial['alt1'], trial['alt1'], self.stimuli_positions[0], stimuli[1])
            alt1.draw()
            # alt2
            alt2 = self.present_stimuli(trial['alt2'], trial['alt2'], self.stimuli_positions[1], stimuli[2])
            alt2.draw()
            self.win.flip()

            keys = event.waitKeys(keyList=['x', 'm'])
            self.rt = self.timer.getTime()
            if self.testtype == 'practice':
                if keys[0] != trial['correctresponse']:
                    fixation.setText(u'Fel! Det är färgen som gäller inte ordet')

                else:
                    fixation.setText(u'Rätt!')
                fixation.draw()
                self.win.flip()
                core.wait(2)

            if self.testtype == 'test':
                if keys[0] == trial['correctresponse']:
                    trial['Accuracy'] = 1
                else:
                    trial['Accuracy'] = 0

                trial['RT'] = self.rt
                trial['Response'] = keys[0]
                trial['Sub_id'] = self.experiment_info['Subid']
                trial['Sex'] = self.experiment_info['Sex']
                writeCsv(self.experiment_info[u'DataFile'], trial)

            event.clearEvents()


def display_instructions(start_instruction=''):
    # Display instructions
    instructions = loadFiles('instructions', '.txt', 'text', window)
    if start_instruction == 'Practice':
        instructions['instructions_SWE'].pos = (0.0, 0.5)
        instructions['instructions_SWE'].draw()

        positions = [[-.2, 0], [.2, 0], [0, 0]]
        examples = [experiment.create_text_stimuli() for pos in positions]
        example_words = ['green', 'blue', 'green']
        if settings['Language'] == 'Swedish':
            example_words = [swedish_task(word) for word in example_words]

        for i, pos in enumerate(positions):
            examples[i].pos = pos
            if i == 0:
                examples[0].setText(example_words[i])
                examples[0].setColor('Green')
            elif i == 1:
                examples[1].setText(example_words[i])
            elif i == 2:
                examples[2].setColor('Green')
                examples[2].setText(example_words[i])
        [example.draw() for example in examples]

        instructions['instructions2_SWE'].pos = (0.0, -0.5)
        instructions['instructions2_SWE'].draw()
    elif start_instruction == 'Test':
        instructions['questions_SWE'].draw()

    elif start_instruction == 'End':
        instructions['experiment_done_SWE'].draw()

    window.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()


def swedish_task(word):
    swedish = '+'
    if word == "blue":
        swedish = u"blå"

    elif word == "red":
        swedish = u"röd"

    elif word == "green":
        swedish = u"grön"

    elif word == "yellow":
        swedish = "gul"

    return swedish


if __name__ == "__main__":
    experiment = Experiment()
    settings = experiment.settings()
    window = experiment.create_window(color=(0, 0, 0))
    # We don't want the mouse to show:
    event.Mouse(visible=False)
    # Practice Trials
    display_instructions(start_instruction='Practice')

    practice = experiment.create_trials('practice_list.csv')
    experiment.running_experiment(practice, testtype='practice')
    # Test trials
    display_instructions(start_instruction='Test')
    trials = experiment.create_trials('stimuli_list.csv')
    experiment.running_experiment(trials, testtype='test')

    # End experiment but first we display some instructions
    display_instructions(start_instruction='End')
    window.close()
