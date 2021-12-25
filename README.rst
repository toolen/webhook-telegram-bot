webhook-telegram-bot
=======================
.. image:: https://github.com/toolen/webhook-telegram-bot/actions/workflows/ci.yaml/badge.svg?branch=master
    :target: https://github.com/toolen/webhook-telegram-bot/actions/workflows/ci.yaml
    :alt: CI Status

Telegram bot for handling webhook requests.

Supported repositories
======================

Bitbucket
-----------------

Repository events:
 - repo:push
 - repo:commit_comment_created
 - repo:commit_status_updated

Pull request events:
 - pullrequest:created
 - pullrequest:updated
 - pullrequest:approved
 - pullrequest:unapproved
 - pullrequest:fulfilled
 - pullrequest:rejected
 - pullrequest:comment_created
 - pullrequest:comment_updated