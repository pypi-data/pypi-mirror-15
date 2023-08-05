### lsoc / LS OCTAL ###
A lite Pyhton package that lets you view file and directory access rights with octal.

Equivilant to typing: stat -c "%a %n" *

Like this:
 alper >~> lsoc
755 Desktop
755 Documents
755 Downloads
755 Music
600 myfile.tar.gz
755 Pictures
755 Public
400 Python.pem
775 Steam

 alper >~> lsoc /usr/bin/sudo
4755 /usr/bin/sudo
4755 /usr/bin/sudo

