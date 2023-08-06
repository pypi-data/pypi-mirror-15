VM monitoring probe 
VM monitoring client is used in order to gather monitoring data from VM's linux kernel (/proc/stat/, /proc/dev/net etc) and push them to monitoring server. 
The url of the pushgateway monitoring server must be set in node.conf file 

Supported monitoring metrics are:
 * cpu usage
 * memory usage
 * disk usage 
 * network traffic

Dependencies:
 * python 2.7
 
Run monitoring client:
export PW_URL=http://pushgateway:9091/metrics
export ND_NAME=TEST_VNF
sudo python run.py

