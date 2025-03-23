from dict.dict_util import load_dict
from dict.word import Word, Writing, WritingList, Reading, ReadingList, Translation, TranslationList, Example, WordList
from dict.treeDict import AhoTree

class Dictionary():
    def __init__(self, xmlDictionaries:list):
        wordList = WordList([])
        for xmlDictionary in xmlDictionaries:
            wordList.extend(JMdictToWordList(xmlDictionary))
        self.tree = AhoTree(wordList)
        self.wordSet = self.tree.set
        
    def search(self, query_word:str):
        query = query_word.strip()
        return self.tree.get_words(query)[0]
        
    def __str__(self):
        string = f'{self.tree}'
        return string
    
    def get_node(self):
        return self.tree.get_node()
        


def JMdictToWordList(xmlDictionary, isDebug=False):
    wordList = WordList([])
    for entry in xmlDictionary:
        writings = WritingList()
        readings = ReadingList()
        translations = TranslationList()
        for child in entry:
            match child.tag:
                case 'k_ele':
                    writing = Writing()
                    for grandchild in child:
                        match grandchild.tag:
                            case 'keb':
                                writing.writing = grandchild.text
                            case 'ke_inf':
                                writing.notes = grandchild.text
                            case 'ke_pri':
                                writing.priority = grandchild.text
                            case _:
                                print(f'Skipped field {grandchild.tag} in k_ele') if isDebug else None
                    writings.append(writing)
                case 'r_ele':
                    hasK = True if entry.find('k_ele') is not None else False
                    reading = Reading()
                    for grandchild in child:
                        match grandchild.tag:
                            case 'reb':
                                if not hasK:
                                    writings.append(Writing(grandchild.text))
                                reading.reading = grandchild.text
                            case 're_inf':
                                reading.notes = grandchild.text
                            case 're_pri':
                                reading.priority = grandchild.text
                            case 're_nokanji':
                                reading.nokanji = grandchild.text
                            case 're_restr':
                                reading.applies_to = grandchild.text
                            case _:
                                print(f'Skipped field {grandchild.tag} in r_ele') if isDebug else None
                    readings.append(reading)
                case 'sense' | 'trans':
                    translation = Translation()
                    translation.notes=' '
                    for grandchild in child:
                        match grandchild.tag:
                            case 'gloss' | 'trans_det':
                                translation.translation = grandchild.text
                            case 'stagk' | 'stagr':
                                translation.notes = translation.notes + ' Only applies to' + grandchild.text
                            case 'xref':
                                translation.ref = grandchild.text
                            case 'pos' | 'name_type':
                                translation.pos = grandchild.text
                            case 'field':
                                translation.field = grandchild.text
                            case 'misc':
                                translation.notes = translation.notes + ' ' + grandchild.text
                            case 'lsource':
                                translation.notes = translation.notes + f" Borrowed from {grandchild.attrib} original word: {grandchild.text}"
                            case 'dial':
                                translation.dialect = grandchild.text
                            case 's_inf':
                                translation.notes = translation.notes + f' {grandchild.text}'
                            case 'example':
                                translation.example = Example(grandchild.find('ex_srce').text, grandchild.find('ex_text').text, 
                                                              [sentence.text for sentence in grandchild.findall('ex_sent')])
                            case _:
                                print(f'Skipped field {grandchild.tag} in {child.tag}') if isDebug else None
                    translations.append(translation)
        wordList.append(Word(writings, readings, translations))
    return wordList   
