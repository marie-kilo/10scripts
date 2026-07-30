#!/usr/bin/env bash

python -m venv env
source env\Scripts\activate
pip install -r requirements.txt

# ~/.pyenv/pyenv-win/versions/3.14.2/python.exe -m venv env


# .env porte les secrets locaux, il est ignoré par git ; l'exemple, lui, est versionné
cp -n .env.example .env || true

python config.py
