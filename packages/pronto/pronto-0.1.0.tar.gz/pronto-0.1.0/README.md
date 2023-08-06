# pronto : **P**ython f**ron**tend **t**o **O**ntologies

#### Overview
PROnto is a python module to parse, analyse and explore ontologies in some popular formats. For now, **obo** and **owl/xml** were added, but more formats are to be added in the future (you can even add your own to work with the current API).


#### Installation
Installing with pip is the easiest:
```bash
pip install pronto          # if you have the admin rights
pip install pronto --user   # if you want to install it for only one user
```

If for some reason you do not like `pip`, you can also clone the repository and install it with the setup script (still requires `setuptools`):
```bash
git clone https://github.com/althonos/pronto
cd pronto
python3 setup.py install    # may also require admin rights
```


#### Usage
Currently there are 2 classes which both inherit from Ontology: **Obo** and **OwlXML**. To parse the right kind of file you have to use the right class, although that will probably change to the future to provide an unique **Ontology** class. Right now though you can still use the Ontology class as a base to merge other ontologies into.

Instantiate an obo ontology and getting a term by accession number:
```python
import pronto
ont = pronto.Obo('path/to/file.obo')
term = ont['REF:ACCESSION']
```

Display an ontology in obo format and in json format:
```python
import pronto
ont = pronto.OwlXML('https://net.path.should/work/too.owl')
print(ont.obo)
print(ont.json)
```

Merge two ontologies:
```python
import pronto
nmr = pronto.OwlXML('https://raw.githubusercontent.com/nmrML/nmrML/'
                    'master/ontologies/nmrCV.owl')
ms  =    pronto.Obo('http://psidev.cvs.sourceforge.net/viewvc/psidev/psi'
                    '/psi-ms/mzML/controlledVocabulary/psi-ms.obo')

ms.merge(nmr) # MS ontology keeps its metadata but now contains NMR terms
              # as well.

assert('NMR:1000004' in ms)
```

Explore every term of an ontology and print those with children:
```python
import pronto
ont = pronto.Obo('path/to/file.obo')
for term in ont:
    if term.children:
        print(term)
```


#### Design

###### Reference
Any **Term** of an **Ontology** can have relationships to other Terms. Those relationships can be *referenced* (the .relations dictionnary of Terms containing Terms) or *plain* (the .relations dictionnary containing only the id of the other Terms).

A referenced ontology will be able to do the following:
```python
ont = Ontology('path/to/file.owl', referenced=True) #default

for term in ont:
   for child in term.relations['can_be']: # can be is the inverse of is_a
       print(child.name)
```
whereas a plain ontology will need the complete ontology to have access to terms the relations references to:
```python
ont = Ontology('/path/to/file.owl', reference=False)

for term in ont:
    for part in term.relations['has_part']: # has_part is the inverse of       
                                            # part_of and is_part
        print(ont[part].name) 

```

When mergeing two ontologies, if of the two is referenced then ***the merged ontology will become referenced as well !***

#### TODO
* write a proper documentation
* create a proper relationship class
* test with many different ontologies
* extract data from OwlXML where attributes are ontologic terms
* extract metadatas from OwlXML
* add other owl serialized formats
* (maybe) add serialization to owl

