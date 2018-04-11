# Data Processing Pipeline for KBCommons
This data processing pipeline is a TCP/IP server that allows front-end or remote client to submit their job. For now, the pipeline contains five automated sub-pipelines (cDNA reformat, CDS reformat, Protein Sequence reformat, Annotation processing, Gene information processing, gene expression data and differential expression data processing). Once the data processing done, the pipeline would create new appropriate table and then upload data to it automatically.

# Flowchart
Following figure is the flowchart of this pipeline:
![alt text](https://raw.githubusercontent.com/shuaizengMU/Google-Interview-KBCommon-Pipeline-Python/master/images/Untitled%20Diagram.png "Flowchart of pipeline")


# Installation

- Download data processing pipeline by
```
git clone https://github.com/shuaizengMU/Google-Interview-KBCommon-Pipeline-Python.git
```

- Revise the mysql configuration file
```sh
cd ./config/
vi ./mysql_config.json
```

Add your database user and password on mysql_config.json file.
```
{
  "test_db": {
    "host": "localhost",
    "user": "KBCommons",
    "passwd": "Your Password",
    "port": 3306,
    "db": "Test"
  }
}
```

- Revise the mysql configuration file
```sh
cd ./config/
vi ./server_config.json
```

Add your server TCP information in server_config.json.
```
{
  "server" : {
    "TCP_IP"      : "127.0.0.1",
    "TCP_PORT"    : 6666,
    "BUFFER_SIZE" : 1024,
    "LOG_DIR"     : "./log/"
  }
}
```

- Installation has been tested in Linux and Mac OS X with Python 2.7.
- Since the package is written in python 2.7, python 2.7 with the pip tool must be installed first. The pipeline uses the following dependencies: numpy, scipy, pandas, orator. You can install these packages first, by the following commands:
```
pip install pandas
pip install numpy
pip install scipy
pip install orator
```

# Running

- Since the pipeline is TCP/IP server, you need to run the main server before processing your data. Following is the example of command.
```
python ./server_main.py
```

# Home Page of KBCommons

- If your are interested in KBCommons project, we are very welcome you to visit our website below.
```
http://kbcommons.org/
```

# Contact
Author: Shuai Zeng ( cengsai@gmail.com or zengs@mail.missouri.edu )



