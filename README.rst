repository-telegram-bot
=======================
.. image:: https://github.com/toolen/repository-telegram-bot/actions/workflows/ci.yaml/badge.svg?branch=master
    :target: https://github.com/toolen/repository-telegram-bot/actions/workflows/ci.yaml
    :alt: CI Status

Telegram bot for notification of all changes in your repositories.

Supported repositories
======================

Bitbucket
-----------------

Repository events:
 - repo:push
 - repo:updated

Pull request events:
 - pullrequest:created
 - pullrequest:updated
 - pullrequest:approved
 - pullrequest:unapproved
 - pullrequest:fulfilled
 - pullrequest:rejected
 - pullrequest:comment_created
 - pullrequest:comment_updated