#!/bin/bash
solr-5.1.0/bin/solr start
solr-5.1.0/bin/solr delete -c af-search
solr-5.1.0/bin/solr create -c af-search

solr-5.1.0/bin/post -c af-search db/

cp stopwords.txt solr-5.1.0/server/solr/af-search/conf
