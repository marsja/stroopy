import codecs
import csv
import glob
import os

from psychopy import visual


def loadFiles(directory, exts, filetype, win='', whichfiles='*', stimlist=[]):
    """ Load text intstructions"""
    path = os.getcwd()
    if isinstance(exts, list):
        filelist = []
        for currextension in exts:
            filelist.extend(glob.glob(
                os.path.join(path, directory, whichfiles + currextension)))
    else:
        filelist = glob.glob(os.path.join(path, directory, whichfiles + exts))
        filematrix = {}

    for num, curfile in enumerate(filelist):
        fullpath = curfile
        fullfilaname = os.path.basename(fullpath)
        stimfile = os.path.splitext(fullfilaname)[0]

        if filetype == 'text':
            with codecs.open(fullpath, 'r', encoding='latin-1') as f:
                textRef = visual.TextStim(win, text=f.read(), wrapWidth=1.2, alignHoriz='center', color="Black",
                                          alignVert='center', height=0.06)

            filematrix[stimfile] = ((textRef))

    return filematrix


def writeCsv(fileName, thisTrial):
    fullPath = os.path.abspath(fileName)
    if not os.path.isfile(fullPath):
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.keys())
            csv.writer(f, delimiter=';').writerow(thisTrial.values())
    else:
        with codecs.open(fullPath, 'ab+', encoding='utf8') as f:
            csv.writer(f, delimiter=';').writerow(thisTrial.values())
