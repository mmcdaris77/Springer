#!/bin/bash
echo "Starting the Producer........."

cd opt/kafka_2.13-2.8.1/bin
kafka-console-producer.sh -topic quickstart -bootstrap-server localhost:9092

