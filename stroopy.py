# -*- coding: utf-8 -*-
import codecs
import csv
import glob
import os

from psychopy import visual, event, core, data, gui


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

    def create_text_stimuli(self, text='', pos=[0.0, 0.0], name='', color='Black'):
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
        textStim = visual.TextStim(win=self.win, ori=0, name=self.name,
                                   text=self.text, font=u'Arial',
                                   pos=self.pos,
                                   color=self.color, colorSpace=u'rgb')
        return textStim

    def create_trials(self, trial_file, randomization='random'):
        '''Doc string'''
        self.trial_file = trial_file
        self.random = randomization
        self.data_types = ['Response', 'Accuracy', 'RT', 'Sub_id', 'Sex']
        with open(self.trial_file, 'rb') as stimfile:
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
            print "Swedish version"
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
                writeCsv('test.csv', trial)

            event.clearEvents()


def loadFiles(directory, exts, fileType, win='', whichFiles='*', stimList=[]):
    """ Load text intstructions"""
    path = os.getcwd()
    if isinstance(exts, list):
        fileList = []
        for curExtension in exts:
            fileList.extend(glob.glob(
                os.path.join(path, directory, whichFiles + curExtension)))
    else:
        fileList = glob.glob(os.path.join(path, directory, whichFiles + exts))
        fileMatrix = {}

    for num, curFile in enumerate(fileList):
        fullPath = curFile
        fullFileName = os.path.basename(fullPath)
        stimFile = os.path.splitext(fullFileName)[0]

        if fileType == 'text':
            with codecs.open(fullPath, 'r', encoding='latin-1') as f:
                textRef = visual.TextStim(win, text=f.read(), wrapWidth=1.2, alignHoriz='center', color="Black",
                                          alignVert='center', height=0.06)

            fileMatrix[stimFile] = ((textRef))

    return fileMatrix


def writeCsv(fileName, thisTrial):
    fullPath = os.path.abspath(fileName)
    if not os.path.isfile(fullPath):
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.keys())
            csv.writer(f, delimiter=';').writerow(thisTrial.values())
    else:
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.values())


def display_instructions(start_instruction=True):
    # Display instructions
    instructions = loadFiles('instructions', '.txt', 'text', window)
    if start_instruction == True:
        instructions['instructions_SWE'].pos = (0.0, 0.5)
        instructions['instructions_SWE'].draw()

        positions = [[-.2, 0], [.2, 0], [0, 0]]
        examples = experiment.create_text_stimuli(window, text=u'Grön')
        for i, pos in enumerate(positions):
            examples.pos = pos
            if i == 0:
                examples.setText(u'Grön')
            else:
                examples.setText(u'Blå')
            if i == 2:
                examples.setColor('Green')
            examples.draw()

        instructions['instructions2_SWE'].pos = (0.0, -0.5)
        instructions['instructions2_SWE'].draw()
    else:
        instructions['questions_SWE'].draw()

    window.flip()
    event.waitKeys(keyList=['space'])
    event.clearEvents()


def swedish_task(word):
    swedish = '+'
    if word == "blue":
        swedish = u"Blå"

    elif word == "red":
        swedish = u"röd"

    elif word == "green":
        swedish = u"grön"

    elif word == "yellow":
        swedish = "gul"

    return swedish


####
experiment = Experiment()
experiment.settings()
window = experiment.create_window()
# Practice Trials
display_instructions()

practice = experiment.create_trials('practice_list.csv')
experiment.running_experiment(practice, testtype='practice')
# Test trials
display_instructions(start_instruction=False)
trials = experiment.create_trials('stimuli_list.csv')
experiment.running_experiment(trials, testtype='test')

core.wait(.2)
window.close()
