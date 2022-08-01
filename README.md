# unlock-spbstu-cxx-test
Fast and minimal setup for testing your labs

## Install
Скачайте репозиторий и запустите программу, укажите пусть до лабы
```bash
git clone git@github.com:michael2to3/unlock-spbstu-cxx-test.git
python ./main.py ../spbspu-labs-aads-904-a/gaile.michael/T3
```

Отчет о проделанных тестах находиться в корне форка
```bash
cat dist/acceptance.xml
```

## Usage
Examples:
```bash
$ python ../unlock/main.py gaile.michael/T1 # запустить от родительского каталога
$ python main.py ../spbspu-labs-aads-904-a/gaile.michael/S0/ # запустить с полным указанием пути к лабе
$ python out/main.py gaile.michael/S3 # скопировать в out
```
