venv\Scripts\pyuic5.exe src\main\python\cguis\design\main_window.ui -o src\main\python\cguis\design\main_window.py
venv\Scripts\pyuic5.exe src\main\python\cguis\design\scroll_cube.ui -o src\main\python\cguis\design\scroll_cube.py
venv\Scripts\pyuic5.exe src\main\python\cguis\design\settings_dialog.ui -o src\main\python\cguis\design\settings_dialog.py

venv\Scripts\pyrcc5.exe src\main\python\cguis\resource\view_rc.qrc -o src\main\python\cguis\resource\view_rc.py

venv\Scripts\pylupdate5.exe src\main\python\main.py src\main\python\wgets\channel.py src\main\python\wgets\graph.py src\main\python\wgets\operation.py src\main\python\wgets\rule.py src\main\python\wgets\settings.py src\main\python\cguis\design\main_window.py src\main\python\cguis\design\settings_dialog.py -ts src\main\python\cguis\lang\en.ts
venv\Scripts\pylupdate5.exe src\main\python\main.py src\main\python\wgets\channel.py src\main\python\wgets\graph.py src\main\python\wgets\operation.py src\main\python\wgets\rule.py src\main\python\wgets\settings.py src\main\python\cguis\design\main_window.py src\main\python\cguis\design\settings_dialog.py -ts src\main\python\cguis\lang\zh.ts
