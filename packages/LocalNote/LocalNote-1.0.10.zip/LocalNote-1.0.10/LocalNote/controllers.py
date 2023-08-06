import os, time, re

import chardet

from local import Storage as LocalStorage
from local import html2text, markdown
from evernoteapi.controller import EvernoteController

class Controller(object):
    def __init__(self):
        self.ls = LocalStorage()
        self.token, self.isSpecialToken, self.sandbox, self.isInternational, self.expireTime, self.lastUpdate, self.notebooks = self.ls.get_config()
        self.available, self.ec = self.__check_available()
        if self.available:
            self.es = self.ec.storage
            self.ls.maxUpload = self.ec.get_upload_limit()
        self.changesList = []
    def __check_available(self):
        if not self.isSpecialToken and self.expireTime < time.time(): return False, None
        if self.token == '': return False, None
        try:
            ec = EvernoteController(self.token, self.isSpecialToken, self.sandbox, self.isInternational, self.notebooks)
            self.ls.update_config(self.token, self.isSpecialToken, self.sandbox, self.isInternational,
                    self.expireTime, self.lastUpdate, self.notebooks)
            return True, ec
        except:
            return False, None
    def log_in(self, config = {}, **kwargs):
        config = dict(config, **kwargs)
        if config.get('token') is not None: self.token = config.get('token')
        if config.get('isSpecialToken') is not None: self.isSpecialToken = config.get('isSpecialToken')
        if config.get('sandbox') is not None: self.sandbox = config.get('sandbox')
        if config.get('isInternational') is not None: self.isInternational = config.get('isInternational')
        if config.get('expireTime') is not None: self.expireTime = config.get('expireTime')
        if config.get('lastUpdate') is not None: self.lastUpdate = config.get('lastUpdate')
        if config.get('notebooks') is not None: self.notebooks = config.get('notebooks')
        available, ec = self.__check_available()
        if available:
            self.available = True
            self.ec = ec
            self.es = self.ec.storage
            self.ls.maxUpload = self.ec.get_upload_limit()
        return available
    def fetch_notes(self):
        if not self.available: return False
        self.es.update(self.token, self.ec.noteStore)
        return True
    def __get_changes(self, update = False): # -1 for need download, 1 for need upload, 0 for can be uploaded and downloaded
        if not update: return self.changesList # (fileFullPath, status)
        r = []
        fileDict = self.ls.get_file_dict()
        noteDict = self.es.get_note_dict()
        for nbName, lNotes in fileDict.items():
            eNotes = noteDict.get(nbName)
            if eNotes is None: # notebook exists locally not online
                r.append(([nbName], 0))
                continue
            delIndex = []
            for lNote in lNotes:
                for i, eNote in enumerate(eNotes):
                    if lNote[0] != eNote[0]: continue
                    if self.ls.lastUpdate < lNote[1]: # need upload
                        if self.ls.lastUpdate < eNote[1] and lNote[1] < eNote[1]: # need download
                            r.append(([nbName, lNote[0]], 0))
                        else:
                            r.append(([nbName, lNote[0]], 1))
                    else:
                        if self.ls.lastUpdate < eNote[1] and lNote[1] < eNote[1]:
                            r.append(([nbName, lNote[0]], -1))
                        # else:
                            # debug
                            # r.append(([nbName, lNote[0]], 2))
                    delIndex.append(i)
                    break
                else: # note exists locally not online
                    r.append(([nbName, lNote[0]], 0))
            eNotes = [n for i, n in enumerate(eNotes) if i not in delIndex]
            for eNote in eNotes: r.append(([nbName, eNote[0]], 0)) # note exists online not locally
            del noteDict[nbName]
        for nbName in noteDict.keys(): r.append(([nbName], 0))
        self.changesList = r
        return r
    def get_changes(self):
        return self.__get_changes(True)
    def check_files_format(self):
        return self.ls.check_files_format()
    def download_notes(self, update = True):
        if not self.available: return False
        noteDict = self.es.get_note_dict()
        invalidNoteList = []
        def _download_note(noteFullPath):
            if any(c in ''.join(noteFullPath).decode('utf8') for c in u'\\/:*?"<>|\xa0'):
                invalidNoteList.append(noteFullPath)
                return
            print(('Downloading '+'/'.join(noteFullPath)).decode('utf8'))
            if self.es.get(noteFullPath) is None: # delete note if is deleted online
                self.ls.write_note(noteFullPath, {})
                return
            contentDict = self.ec.get_attachment(noteFullPath)
            if contentDict.get(noteFullPath[1]+'.md') is None:
                if contentDict.get(noteFullPath[1]+'.html') is None:
                    contentDict[noteFullPath[1]+'.html'] = self.ec.get_content(noteFullPath)
                else: # avoid mistaken overwrite of attachment
                    fileNum = 1
                    while 1:
                        if contentDict.get(noteFullPath[1]+'(%s).html'%fileNum) is None:
                            contentDict[noteFullPath[1]+'(%s).html'%fileNum] = contentDict[noteFullPath[1]+'.html']
                            contentDict[noteFullPath[1]+'.html'] = self.ec.get_content(noteFullPath)
                            break
                        else:
                            fileNum += 1
            self.ls.write_note(noteFullPath, contentDict)
        for noteFullPath, status in self.__get_changes(update):
            if status not in (-1, 0):
                continue
            elif any(c in ''.join(noteFullPath).decode('utf8') for c in u'\\/:*?"<>|\xa0'):
                invalidNoteList.append(noteFullPath)
                continue
            elif 1 < len(noteFullPath):
                _download_note(noteFullPath)
            else:
                notes = noteDict.get(noteFullPath[0])
                if notes is None:
                    self.ls.write_note(noteFullPath, {}) # delete folder
                else:
                    self.ls.write_note(noteFullPath, {1}) # create folder
                    for note in notes: _download_note(noteFullPath + [note[0]])
        self.ls.update_config(lastUpdate = time.time() + 1)
        return invalidNoteList or True
    def upload_files(self, update = True):
        if not self.available: return False
        def encode_content(content):
            try:
                content.decode('utf8')
            except:
                try:
                    content = content.decode(chardet.detect(content)['encoding']).encode('utf8')
                except:
                    content = 'Upload encode failed, I\'m sorry! Please contact i7meavnktqegm1b@qq.com with this file.'
            return content
        def _upload_files(noteFullPath, attachmentDict):
            print(('Uploading '+'/'.join(noteFullPath)).decode('utf8'))
            nbName, nName = noteFullPath
            if not attachmentDict:
                self.ec.delete_note(noteFullPath)
            elif nName + '.md' in attachmentDict.keys():
                content = encode_content(attachmentDict[nName+'.md']).decode('utf8')
                self.ec.update_note(noteFullPath, markdown(content).encode('utf8'), attachmentDict)
            elif nName + '.html' in attachmentDict.keys():
                content = encode_content(attachmentDict[nName+'.html'])
                del attachmentDict[nName + '.html']
                self.ec.update_note(noteFullPath, content, attachmentDict)
        for noteFullPath, status in self.__get_changes(update):
            if status not in (1, 0): continue
            if 1 < len(noteFullPath):
                attachmentDict = self.ls.read_note(noteFullPath)
                _upload_files(noteFullPath, attachmentDict)
            else:
                lns = self.ls.get_file_dict().get(noteFullPath[0])
                ens = self.es.get_note_dict().get(noteFullPath[0])
                if lns is None:
                    for note in ens or []: self.ec.delete_note(noteFullPath + [note[0]])
                    self.ec.delete_notebook(noteFullPath)
                else:
                    self.ec.create_notebook(noteFullPath[0])
                    for note in lns:
                        attachmentDict = self.ls.read_note(noteFullPath + [note[0]])
                        _upload_files(noteFullPath + [note[0]], attachmentDict)
        self.ls.update_config(lastUpdate = time.time() + 1)
        return True
def convert_html(htmlDir, force = None):
    # FileName for done, 1 for wrong file type, 2 for file missing
    # 3 for need rename, 4 for unknown encoding
    fileName, ext = os.path.splitext(htmlDir)
    if ext != '.html': return 1
    if not os.path.exists(htmlDir): return 2
    with open(htmlDir, 'rb') as f: content = f.read()
    try:
        content = content.decode('utf8')
    except:
        try:
            content = content.decode(chardet.detect(content)['encoding'])
        except:
            return 4
    if os.path.exists(fileName + '.md'):
        if force is None:
            return 3
        elif force == True:
            pass
        elif force == False:
            index = 1
            while 1:
                if not os.path.exists(fileName + '(%s)'%index + '.md'): break
                index += 1
            fileName += '(%s)'%index
    with open(fileName + '.md', 'wb') as f: f.write(html2text(content).encode('utf8'))
    return fileName + '.md'
