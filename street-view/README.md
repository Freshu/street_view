# Wymaga Pythona 3.5.2, OpenCV 3.1.0 i Panda3D 1.9.2

----
## Jak zainstalowaæ OpenCV?

1. Œci¹gamy jedn¹ z [tych](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv) wersji .whl z bibliotek¹: 

    opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win32.whl
    opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win_amd64.whl

2. Wchodzimy do naszego pythonowego folderu z pipem(Python3\Scripts) i wrzucamy tam pliki .whl .

3. Otwieramy konsolê i wpisujemy:
    pip install <nazwa_pliku>

----
## Jak zainstalowaæ Panda3D?

1. Œci¹gamy i instalujemy SDK 1.9.2 w dowonlym miejscu. 
Ze [strony](https://www.panda3d.org/download.php?platform=windows&version=devel&sdk)
œci¹gamy Panda3D-SDK-1.10.0pre-3eed7bc-py3.5.exe pod Pythona 3.5

2. W miejscu gdzie mamy zainstalowanego Pythona + '\Lib\site-packages' tworzymy plik panda.pth . W œrodku wpisujemy 2 linijki ze œcie¿kami do naszej Pandy3D.

Przyk³adowy plik panda.pth :

    C:\Panda3D-1.10.0
    C:\Panda3D-1.10.0\bin
