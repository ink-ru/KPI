# KPI
You can use it only inside private VPN and only after authorization

## Установка
### apt-get
Многие сталкиваются с тем, что при установке пакета из файла а не из репозитория, зависимости автоматически не устанавливаются, когда вы выполняете команду dpkg -i имя_пакета

Сам dpkg зависимости автоматически устанавливать не умеет (насколько я знаю), но вам поможет вот такая последовательность команд:
```
dpkg -i kpi_1.0_all.deb
apt-get -f install
```
Вторая команда скачивает и устанавливает все зависимости, которых не хватило первой команде, после чего автоматически продолжает установку прерваной установки пакета, т.е. повторно dpkg запускать не требуется.

### gdebi
Другой вариант автоматической уставновки с зависсимостями:
```
$ sudo apt-get install gdebi
$ sudo gdebi-gtk kpi_1.0_all.deb
```

Список зависимостей (dependencies):
```
python-qt4
python3-pyqt4
```

## Сборка пакета
Перед сборкой пакета:
```
sudo apt-get install dpkg
```

Сборка пакета:
```
chmod -R 755 kpi
chmod +x ./kpi/opt/kpi/kpi.py
fakeroot dpkg-deb --build kpi
mv kpi.deb kpi_1.0_all.deb
```

https://github.com/ink-ru/KPI/blob/master/README.md
