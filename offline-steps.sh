#!/bin/sh
set -eu
set -x
./wiki --help
./wiki doctor
./wiki ingest vault/raw --regenerate
./wiki search 'natural monopoly marginal cost fixed cost'
./wiki ask 'According to the notes, should someone buying a commodity in the future hedge with long or short futures?' --mode local
./wiki ask 'According to the notes, why can a natural monopoly lose money when the regulated price equals marginal cost?' --mode local
./wiki ask 'According to the notes, which three aspects of electricity value are ignored by LCOE?' --mode local
./wiki ask 'What is the exact date and classroom for the EEM final exam?' --mode local
printf '%s\n' 'what can we do?' 'what can you help me with?' 'Suggest a short three-step plan for revising a difficult topic.' 'make that shorter' 'For this conversation only, imagine that my project budget is 999 dollars.' '/exit' | ./wiki chat
./wiki ask 'What is my project budget in dollars?' --mode local
./wiki ingest vault/raw
