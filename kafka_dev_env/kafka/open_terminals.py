
import subprocess
import os 

me_dir = os.path.dirname(os.path.realpath(__file__))

consumer_start_sh = os.path.join(me_dir, 'start_consumer.sh')
producer_start_sh = os.path.join(me_dir, 'start_producer.sh')

# make some default cmds
cmd_list = [
    'powershell -NoExit $hr="*"*100'
    ,'write-host $hr'
    ,'write-host ** HELPFUL STUFF **`n*******************'
    ,'write-host ** CD TO FUNCS DIR'
    ,'write-host "`tcd opt/kafka_2.13-2.8.1/bin"'
    ,'write-host ** START CONSUMOR'
    ,'write-host "`tkafka-console-consumer.sh -topic quickstart -from-beginning -bootstrap-server localhost:9092"'
    ,'write-host ** START PRODUCER'
    ,'write-host "`tkafka-console-producer.sh --topic quickstart --bootstrap-server localhost:9092"'
    ,'write-host ** CREATE TOPIC'
    ,'write-host "`tkafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic quickstart"'
    ,'write-host $hr'
]

# open a prompt for the consumer
consumor_cmds = list(cmd_list)
consumor_cmds.append('docker cp {0} kafka:/root/start_consumer.sh'.format(consumer_start_sh))
consumor_cmds.append('docker exec -it kafka /root/start_consumer.sh')
consumor_cmds.insert(2, '$host.ui.RawUI.WindowTitle = "kafka consumer"')
s_cmd = ';'.join(consumor_cmds)
cmd = s_cmd.split()
p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)


# open a prompt for the producer
producer_cmds = list(cmd_list)
producer_cmds.append('docker cp {0} kafka:/root/start_producer.sh'.format(producer_start_sh))
producer_cmds.append('docker exec -it kafka /root/start_producer.sh')
producer_cmds.insert(2, '$host.ui.RawUI.WindowTitle = "kafka producer"')
s_cmd = ';'.join(producer_cmds)
cmd = s_cmd.split()
p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)




