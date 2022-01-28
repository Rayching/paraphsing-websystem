# paraphsing-websystem

線上英文文章改寫系統

此專案調整parrot並且把它線上化，想要看效果的時候有個介面，比較方便


## Quick Start

1. fork the repositories

   ```shell
   git clone https://github.com/Rayching/paraphsing-websystem.git
   ```
2. run the app.py
   ```shell
   uvicorn app:app --reload
   ```

## Development

- Setup virtual environment

```shell
python -m venv your-awesome-venv-name
source your-awesome-venv-name/bin/activate
pip install -r requirements.txt
```

- Start Dev Server

```shell
uvicorn app:app --reload
```

### File Description
```
.
├── requirements.txt 
├── app.py  // 由此程式啟動其他
├── static\js
│   └── para.js
└── templates
    └── para.html 
```
### Result
![Result](https://user-images.githubusercontent.com/44884255/151491868-e3b8d43f-98e1-492c-92f4-d129b4c16287.png)

## Acknowledgement

This theme is an extened work based on [Prithivira](https://github.com/PrithivirajDamodaran/Parrot_Paraphraser#references)

