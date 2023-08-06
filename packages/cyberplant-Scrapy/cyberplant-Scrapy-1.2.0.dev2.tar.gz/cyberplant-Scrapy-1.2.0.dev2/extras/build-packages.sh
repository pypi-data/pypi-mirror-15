#!/bin/sh

echo "Installing FPM..."
gem install fpm

fpm --verbose --debug -s python -t deb -n scrapy .

# Disabled for now
# fpm --verbose --debug -s python -t rpm -n scrapy .
