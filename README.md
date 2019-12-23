# YuGiOhBot: Card Generator

Build status: ![](https://travis-ci.org/YuGiOhBot3000/yugiohbot-cloud-run-card-generator.svg?branch=master)

This project sets up the card generator for the YuGiOhBot.

## What it does
This project creates and uploads a Docker container, with a Python Web Scraper running on Google Chrome.
When invoked, the scraper will visit a YuGiOh Card Maker site and create a card with the given and chosen information.
It will then save the image to Cloud Storage and call the [next function](https://github.com/YuGiOhBot3000/yugiohbot-function-upload-card) to upload it.