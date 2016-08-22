# KPI
You can use it only inside privete VPN and only after authorization

Перед сборкой пакета:
```
sudo apt-get install dpkg debconf debhelper lintian
```

Сборка пакета
```
fakeroot dpkg-deb --build supersh
```

Установка пакета
```
sudo dpkg -i kpi_1.0_all.deb
```
