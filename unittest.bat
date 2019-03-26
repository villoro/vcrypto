:: ------------- Unittest + coverage --------------------------------------
nosetests --with-coverage --cover-package=v_crypt --cover-erase --cover-inclusive
pause

:: ------------- Pylint ---------------------------------------------------
pylint test
cd v_crypt
pylint v_crypt
cd..
pause
