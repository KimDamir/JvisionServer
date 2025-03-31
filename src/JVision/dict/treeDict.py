from dict.word import Word
from dict.word import WordList

class TreeNode:
    def __init__(self, text:str, next:dict, words:WordList=WordList([]), suf:dict=None):
        self.text = text
        self.next = next
        self.words = words
        self.suf = suf

    
    def __str__(self):
        string = self.text + '\n'
        for node in self.next.values():
            string += f' {node}'
        return string
            
    def get_children_words(self):
        childrenWords = WordList([])
        if self.words is not None:
            childrenWords.extend(self.words)
        if len(self.text) > 1:
            for child in self.next.values():
                childrenWords.extend(child.get_children_words())
        return childrenWords
    
    def append_word(self, word:Word):
        self.words.append(word)
        
class AhoTree: #Aho-Corasick tree implementation
    def __init__(self, wordsList:WordList):
        self.root = TreeNode('', dict())
        self.set = set()
        for word in wordsList:
            self.add_word(word)
        self.compute_suffix_links(self.root)
        
    def add_word(self, word:Word):
        currentNode = self.root
        for writing in word.writings:
            self.set.add(writing.writing)
            fullNodeText = ''
            for char in writing.writing.strip():
                fullNodeText += char
                if char not in currentNode.next:
                    nextNode = TreeNode(fullNodeText, dict(), [])
                    currentNode.next[char] = nextNode
                currentNode = currentNode.next[char]
                if currentNode.text == writing.writing.strip():
                    currentNode.append_word(word)
                
    def __str__(self):
        string = f'{self.root}'
        return string
        
    def get_words(self, query:str, max_outer_index=0):
        searchRes = WordList([])
        currentNode = self.root
        index = 0
        for char in query.strip():
            index += 1
            if char in currentNode.next.keys():
                currentNode = currentNode.next[char]
                if currentNode.text == query.strip():
                    searchRes = currentNode.get_children_words()
                    break
            else:
                if (index >= len(query.strip())):
                    break
                if currentNode.suf is not None and query[index-1].strip() in currentNode.suf.keys():
                    searchRes = self.get_words(query[index-1:].strip(), index)[0] + searchRes
                break
            if currentNode.next is None or currentNode.words is not None:
                if max_outer_index == 0 or max_outer_index < index:
                    searchRes = currentNode.get_children_words() + searchRes
                elif max_outer_index == index:
                    searchRes.extend(currentNode.get_children_words())
        return [searchRes, index]
    
    def compute_suffix_links(self, node:TreeNode):
        suffix = node.text[1:] if len(node.text) >= 2 else ''
        if node != self.root:
            node.suf = self.root.next if suffix == '' else self.get_connections(suffix)
        else:
            node.suf = None
        if node.suf is not None or node == self.root:
            for char, childNode in node.next.items():
                self.compute_suffix_links(childNode)
            
    
    def get_connections(self, nodeText:str):
        currentNode = self.root
        if nodeText == '': 
            return currentNode.next
        for char in nodeText:
            if char not in currentNode.next:
                return None
            currentNode = currentNode.next[char]
            if currentNode.text == nodeText:
                return currentNode.next
            
    def get_node(self, nodeText:str):
        currentNode = self.root
        for char in nodeText:
            if char not in currentNode.next:
                return None
            currentNode = currentNode.next[char]
            if currentNode.text == nodeText:
                return currentNode
            
    def get_suffix(self, nodeText:str):
        currentNode = self.root
        if nodeText == '': 
            return currentNode.next
        for char in nodeText:
            if char not in currentNode.next:
                return None
            currentNode = currentNode.next[char]
            if currentNode.text == nodeText:
                return currentNode.suf
            
    
    