
class Reading:
    def __init__(self, reading:str=None, priority:str=None, nokanji: str = None, applies_to:str=None, notes:str=None):
        self.reading=reading
        self.priority=priority
        self.nokanji=nokanji
        self.applies_to = applies_to
        self.notes = notes
        
    def __str__(self):
        string = self.reading
        if self.priority is not None:
            string += ' priority:' + self.priority
        if self.nokanji is not None:
            string += ' No kanj (real) form:' + self.nokanji
        if self.applies_to is not None:
            string += ' Only applies to:' + self.applies_to
        if self.notes is not None:
            string += ' ' + self.notes
            
        return string
            
class ReadingList(list):
    def __init__(self):
        super().__init__()
    
    def append(self, item:Reading):
        super().append(item)
    
    def __str__(self):
        result = str()
        for i in range(len(self)):
            result = f'{self[i]}  '
            
        return result
    
class Writing:
    def __init__(self, writing:str=None, priority:str=None, notes:str=None):
        self.writing=writing
        self.priority=priority
        self.notes = notes
        
    def __str__(self):
        string = self.writing
        if self.priority is not None:
            string += ' priority:' + self.priority
        if self.notes is not None:
            string += ' ' + self.notes
        return string
            
class WritingList(list):
    def __init__(self):
        super().__init__()
    
    def append(self, item:Writing):
        super().append(item)
    
    def __str__(self):
        result = str()
        for i in range(len(self)):
            result = f'{self[i]}  '
            
        return result
    
class Example:
    def __init__(self, source:str, form:str, examples:list):
        self.source = source
        self.form = form
        self.examples = examples
    def __str__(self):
        string = f'Examples: with {self.form} from {self.source}\n'
        for example in self.examples:
            string += f'{example}\n'
        return string
    
class Translation:
    def __init__(self, translation:str=None, ref:str=None, pos: str = None, field:str=None, dialect:str=None, notes:str=None, example:Example=None):
        self.translation=translation
        self.ref=ref #Reference to related words
        self.pos=pos #Part of speech
        self.field = field #Field of use of the meaning
        self.dialect = dialect
        self.notes = notes
        self.example = example
        
    def __str__(self):
        string = ''
        if self.pos is not None:
            string += '(' + self.pos + ') '
        if self.translation is not None:
            string += self.translation + '\n'
        if self.ref is not None:
            string += ' see also:' + self.ref
        if self.field is not None:
            string += ' field:' + self.field
        if self.dialect is not None:
            string += ' dialect:' + self.dialect
        if self.notes is not None:
            string += ' ' + self.notes
        if self.example is not None:
            string += f'\n{self.example}'
        return string
            
class TranslationList(list):
    def __init__(self):
        super().__init__()
    
    def append(self, item:Translation):
        super().append(item)
    
    def __str__(self):
        result = str()
        for i in range(len(self)):
            result += f'{i+1}) {self[i]}\n'
            
        return result
       

class Word:
    def __init__(self, writings:WritingList, readings:ReadingList, translations:TranslationList):
        self.writings = writings
        self.readings = readings
        self.translations = translations
    
    def __str__(self):
        return f'{self.writings}\n{self.readings}\n{self.translations}'
        
class WordList(list):
    def __init__(self, words:list):
        super().__init__(words)
    
    def append(self, object:Word):
        return super().append(object) 
    
    def __str__(self):
        result = str()
        for word in self:
            result += f'{word}\n'
        return result
