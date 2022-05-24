# Polynomials
## Приложение с графическим интерфейсом для подсчёта некоторых многочленов по графам

Разделена на две части: графический интерфейс и программный код. 

Зависимости:
1. `PyQt5`
2. `sympy`
3. `networkx`

Запуск с помощью Python:
```bash
python3 -m pip install -r requirements.txt
python3 src/main.py
```

Компиляция в исполняемый файл:

```bash
pyinstaller --onefile --windowed src/main.py
./dist/main 
```
