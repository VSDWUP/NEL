# NEL Method

## Installing required packages:

### 1. DeepPavlov
Open-source conversational AI library built on PyTorch.
```no-highlight
pip install -q deeppavlov
```
Docs: http://docs.deeppavlov.ai/en/master/

#### 1.1 Installing DeepPavlov NER model
```no-highlight
python -m deeppavlov install <model_name>  
```
Before the first run of deeppavlov NER model you need to build in .py file:
```no-highlight
ner_model = build_model('<ner_model>', download=True, install=True)
```
After completing the build process, download ad install arguments needs to be deleted.

More information about models: https://docs.deeppavlov.ai/en/master/features/models/NER.html

### 2. Razdel
Open-source library, which provides rule-based system for Russian sentence and word tokenization
```no-highlight
pip install razdel
```
Docs: https://github.com/natasha/razdel

### 3. pymystem3
Morphological analyzer for word lemmatization
```no-highlight
pip install pymorphy2
```
Docs: https://pypi.org/project/pymystem3/

### 4. psycopg2
The most popular PostgreSQL database adapter
```no-highlight
pip install psycopg2
```
Docs: https://www.psycopg.org/docs/

### 5. sqlalchemy
Open-source SQL toolkit and object-relational mapper
```no-highlight
pip install sqlalchemy
```
Docs: https://docs.sqlalchemy.org/en/20/

### 6. requests
Library for working with HTTP requests
```no-highlight
pip install requests
```
Docs: https://requests.readthedocs.io/en/latest/


### 7. thefuzz
Library for string matching based on Levenshtein distance
```no-highlight
pip install thefuzz[speedup]
```
Docs: https://github.com/seatgeek/thefuzz
