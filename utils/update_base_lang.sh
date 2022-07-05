#!/usr/bin/env bash

pybabel extract ../. -o ../searx/translations/source/LC_MESSAGES/messages.po -F ../babel.cfg
#pybabel compile -d ../searx/translations