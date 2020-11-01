#!/usr/bin/env bash
set -e
case $1 in
web)
  echo "Deploy web"
  ;;
worker)
  echo "Deploy worker"
  ;;
*)
  echo "Fail!"
  ;;
esac