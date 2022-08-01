# unlock-spbstu-cxx-test
Fast and minimal setup for testing your labs

## Install
Скопируйте репозиторий в родительскую директорию рядом с вашим форком репозитория
```bash
git clone git@github.com:michael2to3/unlock-spbstu-cxx-test.git
```
Перейдите в ваш репозиторий и запустите программу
```bash
cd ./spbspu-labs-aads-904-a
python ../unlock/main.py gaile.michael/T2```

Отчет о проделанных тестах находиться в корне форка
```bash
cat dist/acceptance.xml
```

## Usage
Examples:
```bash
$ python ../unlock/main.py gaile.michael/T1
$ python ../unlock/main.py gaile.michael/S3/
$ python ../unlock/main.py gaile.michael/S0
```
