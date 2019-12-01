# Invoice Date Extractor

Python Flask based REST API Server and a REST Client based on Python Requests Library for systematic extraction of the date from the image of an invoice. The server uses the Google Cloud Vision API for accurate text extraction. The input to file is the base_64 image content and output is the date extracted by the API in YYYY-MM-DD format.

## Getting Started

The following instructions will help you to get a copy of the project on your EC2 server and install required softwares. 

### Prerequisites

AWS Account

### Installing

Create a t2.micro EC2 Ubuntu 18.04 Server.  
Enable inbound port 5000 in security group. ( and port 22 for SSH )   
Once the EC2 server is up and running SSH to it on port 22 and install following packges.   

```
sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
pip3 install flask
pip3 install --upgrade google-cloud-vision

```

Clone git repo on root directory 

```
cd /home/ubuntu
git clone https://github.com/sanjiv96/invoice-date-extractor.git

```

## Google Cloud Platform Settings 

You should have a GCP account with billing enabled ( Trial account has $300 credits ) .  
The following instructions will help you to configure GCP. 

```
Login to Google Cloup Platform and goto Console.  
Create a project.   
Create a service account and download the key file in json format.  
Store this private key in home directory of EC2 server created in previous step as 'key.json' ( /home/ubuntu/key.json ) . 
Enable Cloud Vision API.  

```

How to create Service Account ? 

```
Open the Service Accounts page in the Cloud Console.
Click Select a project.
Select your project and click Open.
Click Create Service Account.
Enter a service account name (friendly display name), an optional description, select a role you wish to grant to the service account, and then click Save.
```

## Deployment

SSH to EC2 instance and create a systemd daemon service.   
  
```
sudo vi /etc/systemd/system/invoice-date-extractor.service  
```
Save following content in the file 

```
[Unit]
Description=Invoice Date Extractor 

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/invoice-date-extractor
Environment="GOOGLE_APPLICATION_CREDENTIALS=/home/ubuntu/key.json"
ExecStart=/usr/bin/python3 server.py
Restart=always

[Install]
WantedBy=multi-user.target

```
Now execute following commands to enable service and start it. 
```
sudo systemctl daemon-reload
sudo systemctl enable invoice-date-extractor.service
sudo systemctl start invoice-date-extractor.service
sudo systemctl status invoice-date-extractor.service
```
The status should show that the service is up and running. 

## Testing Server using Python Client Code. 

Explain what these tests test and why

```
Give an example
```

## DEMO SERVER

### REST Endpoint

Demo server rest endpoint url is : 

```
http://52.27.172.222:5000/extract_date
```

You can send a POST request to above URL with payload like below .  
```
{"base_64_image_content":"add base64 content of the invoice image here"} 
```
The ContentType of the POST request should be <b>'application/json' .</b>

### REST Client 

Here is example online REST client 

https://reqbin.com/
  
### Sample Invoices 

You can find sample invoice receipts in <b>receipts</b> folder of the repository.

### Base64 Conversion Tool 

Here is a example online service to get base64 content from the image. 

https://base64.guru/converter/encode/image

### Response 

Response is in YYYY-MM-DD format like below.  
```
{
    "date": "2019-05-29"
}
```
Note that the server extracts only the first occurance of any date on the receipt/invoice assuming first occurance of the date is transaction date. 
