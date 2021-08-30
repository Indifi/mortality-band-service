SENTIMENT_TOEKNS = ['delici',
                   'amaz',
                   'best',
                   'love',
                   'great',
                   'ambienc',
                   'hour',
                   'perfect',
                   'awesom',
                   'nice',
                   'light',
                   'good',
                   'ask',
                   'worst',
                   'call',
                   'excel',
                   'manag',
                   'place',
                   'pathet',
                   'quick',
                   'custom',
                   'friend',
                   'enjoy',
                   'disappoint',
                   'even',
                   'definit',
                   'favourit',
                   'minut',
                   'fast',
                   'guy',
                   'sit',
                   'point',
                   'money',
                   'littl',
                   'experi',
                   'know',
                   'coffe',
                   'courteou',
                   'cook',
                   'eat',
                   'deliv',
                   'special',
                   'tri',
                   'pizza',
                   'super',
                   'cold',
                   'authent',
                   'take',
                   'present',
                   'favorit',
                   'ambianc',
                   'valu',
                   'averag',
                   'meal',
                   'dish',
                   'deli',
                   'fresh',
                   'piec',
                   'restaur',
                   'wait',
                   'servic',
                   'recommend'
                   ]

EMPTY_SENTIMENT_SCORE = 0.13161

MORTALITY_BAND_RANGE = [(0, 0.0493),
                        (0.0493, 0.0599),
                        (0.0599, 0.0704),
                        (0.0704, 0.0829),
                        (0.0829,0.0963),
                        (0.0963, 0.1193),
                        (0.1193, 0.1647),
                        (0.1647, 0.1983),
                        (0.1983,0.2315),
                        (0.2315,1)]

BOOL = 'bool'
FLOAT = 'float'
LIST = 'list'
STRING = 'str'
INT = 'int'
BOOL_TRUE_STRINGS = ['true', '1']

PAYLOAD_VARS = [
    ('reviews', 'list'),
    ('zomato_vintage', 'float'),
    ('review_last_12m', 'int'),
    ('restId', 'str'),
]

MISSING_PAYLOAD_DATA = 'Missing payload key - {}'
NULL_PAYLOAD_DATA = 'Null payload key - {}'
INVALID_PAYLOAD_DATA = 'Invalid payload data type for key - {}'

