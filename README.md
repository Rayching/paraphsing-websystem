# paraphsing-websystem

線上英文文章改寫系統

此專案藉由Prithivida撰寫的parrot並且把它線上化


## Quick Start

1. fork the repositories

   ```shell
   git clone https://github.com/Rayching/paraphsing-websystem.git
   ```
2. 
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
    └── para.html // 台北
    
### Result
![Result](https://user-images.githubusercontent.com/44884255/151491868-e3b8d43f-98e1-492c-92f4-d129b4c16287.png)

## References
+ [Prithivira](https://github.com/PrithivirajDamodaran/Parrot_Paraphraser#references)