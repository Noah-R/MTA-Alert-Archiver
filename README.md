MTA Alert Archiver is a data pipeline which archives service alerts from the MTA's real-time API. It runs entirely on Amazon Web Services, using CloudWatch Events to run a Lambda function every five minutes, which fetches and process alerts, then inserts them into a MySQL database running on Relational Database Service.

Build instructions:

    -install pip modules locally

        pymysql
        urllib3
    	protobuf

    -delete extra files
    
        .git
        .gitignore
        README.md
    	__pycache__

    -zip