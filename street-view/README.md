# Wymaga OpenCV 3.1.0 i Pythona 3.5.2

Jak zainstalowa� OpenCV?

1. �ci�gamy jedn� z tych wersji .whl z bibliotek�: http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv

a) opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win32.whl
b) opencv_python-3.1.0+contrib_opencl-cp35-cp35m-win_amd64.whl

2. Wchodzimy do naszego pythonowego folderu z pipem(Python3\Scripts) i wrzucamy tam pliki .whl .

3. Otwieramy konsol� i wpisujemy:
pip install <nazwa_pliku>


Jak zainstalowa� Panda3D?

1. �ci�gamy i instalujemy SDK 1.9.2 w dowonlym miejscu. 
Z tej strony https://www.panda3d.org/download.php?platform=windows&version=devel&sdk
�ci�gamy Panda3D-SDK-1.10.0pre-3eed7bc-py3.5.exe pod Pythona 3.5

2. W miejscu gdzie mamy zainstalowanego Pythona + '\Lib\site-packages' tworzymy plik panda.pth
W �rodku wpisujemy 2 linijki ze �cie�kami do naszej Pandy3D np.:
C:\Panda3D-1.10.0
C:\Panda3D-1.10.0\bin
