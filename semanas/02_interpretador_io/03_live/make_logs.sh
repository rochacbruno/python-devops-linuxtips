#!/bin/bash
# alternative is zcat
# zcat nginx_sample.log.gz > nginx_sample.log
gunzip -c nginx_sample.log.gz > nginx_sample.log
