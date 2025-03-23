import gzip
import xml.etree.ElementTree as ET
from dict.dictionary import Dictionary

def create_dict():
    with gzip.open('/home/kane/JvisionServer/resources/dict/JMdict_e_examp.gz', 'rt') as f:
        JMdictxml =f.read()
    with gzip.open('/home/kane/JvisionServer/resources/dict/JMnedict.xml.gz', 'rt') as f:
        JMnedictxml =f.read()
    JMdict = ET.fromstring(JMdictxml)
    JMnedict = ET.fromstring(JMnedictxml)
    JMdictionary = Dictionary([JMdict, JMnedict])
    return JMdictionary