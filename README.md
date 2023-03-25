# ai_art_creation

A proposed directory structure.

ai_art_creation/
│
├── ai_art_creation/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
|   |   ├── chatgpt_utils.py
|   |   ├── chatgpt.py
│   │   └── dall_e.py
│   │
│   ├── image_processing/
│   │   ├── csv/
│   │   ├── images_processed/
│   │   ├── images_raw/
│   │   ├── __init__.py
│   │   ├── lighting.py
│   │   ├── topaz_gigapixel.py
│   │   └── transparent_png.py
│   │
│   ├── store_integration/
│   │   ├── __init__.py
│   │   ├── etsy.py
│   │   └── redbubble.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
|   ├── test_chatgpt.py
│   ├── test_dall_e.py
│   ├── test_topaz_gigapixel.py
│   ├── test_lighting.py
│   ├── test_scaling.py
│   ├── test_etsy.py
│   └── test_redbubble.py
│
├── .gitignore
├── LICENSE
├── README.md
└── setup.py