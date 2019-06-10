# eRisk 2018

[eRisk 2018](http://erisk.irlab.org/)

Early risk prediction on the Internet

eRisk explores the evaluation methodology, effectiveness metrics and practical applications (particularly those related to health and safety) of early risk detection on the Internet.

The system presented here has been developped for the first task:

Task 1 - Early Detection of Signs of Depression : the challenge consists of sequentially processing pieces of evidence (Social Media entries) and detect early traces of depression as soon as possible.


[CLEF 2018](http://clef2018.clef-initiative.eu/) Workshop

Avignon, 11-14 September 2018 

## Getting Started
```
git clone https://github.com/BigMiners/eRisk2018.git
cd eRisk2018
```
Create a python3.5 environment, install requirements :
```
virtualenv -p python3.5 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Parsing the data
Getting the dataset from eRisk organisers (david.losada@usc.es)
Create a split using `splitter.py` :
```
python -m splitter path/to/data/task1 nb_splits test_ratio
```

## System
Create a copy of `config.cfg.default` named `config.cfg`.
Update `[Data][task]` and `[Data][split]` to match the new values.
The split names can be found in `[Data][task]/splits` and are letter names.

Train the system
```
python -m lda
```

Predict
```
python -m predict output_dir number_of_chunks_to_predict_for
```

## Citing this work
Diego Maupomé, Marie-Jean Meurs

[**Using Topic Extraction on Social Media Content for the Early Detection of Depression**](http://labunix.uqam.ca/~meurs_m/publications/erisk2018_clef.pdf),

Proceedings of the Ninth International Conference of the CLEF Association (CLEF 2018)

```
@inproceedings{maupomemeurs2018,
author = {Diego Maupomé and Marie-Jean Meurs},
booktitle = {Experimental IR Meets Multilinguality, Multimodality, and Interaction. 
Proceedings of the Ninth International Conference of the {CLEF} Association ({CLEF} 2018)},
title = {{Using Topic Extraction on Social Media Content for the Early Detection of Depression}},
address   = {Avignon, France},
year = {2018}
}
```


