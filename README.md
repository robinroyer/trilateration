# trilateration [![Build Status](https://travis-ci.org/robinroyer/trilateration.svg?branch=master)](https://travis-ci.org/robinroyer/trilateration)
Finding best intersection or its nearest point for 3 gateways and the distance traveled by the signal for TDOA/TOA trilateration


test with nose2




les filtres que l'on doit effectuer:

- enlever les gw avec un delta timestamp trop important (3 std par exemple) 

- faire un filtrage statistique sur les resulats en sortie (premutation + analyse statistique des resultats)

-> filtre distance et filtre distance 