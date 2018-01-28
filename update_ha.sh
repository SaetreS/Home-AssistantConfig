#!/bin/bash

source /srv/homeassistant/homeassistant_venv/bin/activate
hassctl update-hass && hassctl config && hassctl restart