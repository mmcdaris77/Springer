#!/bin/bash
echo "Starting the Consumer........."
cd opt/kafka_2.13-2.8.1/bin
kafka-console-consumer.sh -topic quickstart -from-beginning -bootstrap-server localhost:9092

