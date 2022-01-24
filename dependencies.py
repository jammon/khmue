text = """Name: asgiref
Version: 3.4.1
Requires:
Name: black
Version: 21.12b0
Requires: platformdirs, typing-extensions, tomli, pathspec, mypy-extensions, click
Name: click
Version: 8.0.3
Requires:
Name: Django
Version: 4.0
Requires: asgiref, sqlparse
Name: django-debug-toolbar
Version: 3.2.2
Requires: sqlparse, Django
Name: django-widget-tweaks
Version: 1.4.9
Requires:
Name: mypy-extensions
Version: 0.4.3
Requires:
Name: pathspec
Version: 0.9.0
Requires:
Name: platformdirs
Version: 2.4.0
Requires:
Name: six
Version: 1.16.0
Requires:
Name: sqlparse
Version: 0.4.2
Requires:
Name: tomli
Version: 1.2.2
Requires:
Name: typing-extensions
Version: 4.0.1
Requires: """

name = "Name: "
requires = "Requires: "
names = []
required = set()
for line in text.splitlines():
    if line.startswith(name):
        names.append(line.removeprefix(name))
    elif line.startswith(requires):
        required = required.union(line.removeprefix(requires).split(", "))

print("for p in", *(n for n in names if n not in required))
print("do")
print("  pip uninstall $p -y")
print("done")

