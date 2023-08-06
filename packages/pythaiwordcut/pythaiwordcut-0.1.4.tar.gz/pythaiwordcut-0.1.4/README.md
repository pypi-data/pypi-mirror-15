# pythaiwordcut - Thai Wordcut in Python

A simple Thai wordcut written in Python, based on Maximum Matching algorithm by [S. Manabu](http://www.aclweb.org/anthology/E14-4016)
. Uses Lexitron (by [NECTEC](http://www.sansarn.com/lexto/license-lexitron.php)) dictionary as default

> Please note: This project is under development and should not be use in production , all function and interface are subject to change. If you have issue or suggestion please feel free to ask, contribution is also very welcome :)

## Installation

```
pip install pythaiwordcut
```

or

```
git clone https://github.com/zenyai/pythaiwordcut.git
python setup.py install
```

## Usage
```
import pythaiwordcut as pwt

pt = pwt.wordcut(removeRepeat=True, stopword=False, removeSpaces=True, minLength=1, stopNumber=False)
print "|".join(pt.segment(u'ทดสอบการตัดคำ'))
```

* removeRepeat: remove intention insertion spelling error such as (สบายยยยยย)
* stopword: remove word that doesn't add sentiment value
* removeSpaces: remove blank space
* minLength: minimum length of each word
* stopNumber: remove number if exist
