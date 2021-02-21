import json
import boto3
from flask import Flask, request, render_template
import webbrowser

app = Flask(__name__,template_folder='templates')

data = {}

@app.route('/', methods =["GET", "POST"]) 
def UI():
   if request.method == "POST": 
      with open('template1.json') as f:
            data = json.load(f)
      stackname = request.form.get("stackname")  
      dbname = request.form.get("DBName")  
      dbpassword = request.form.get("password")  
      dbroot = request.form.get("DBroot") 
      dbuser = request.form.get("DBuser")  
      instance = request.form.get("instance") 
      key = request.form.get("KeyName")  
      SSHloc = request.form.get("SSHLocation") 
     
      data['Parameters']['DBName']['Default']= dbname
      data['Parameters']['DBPassword']['Default']= dbpassword
      data['Parameters']['DBRootPassword']['Default']= dbroot
      data['Parameters']['DBUser']['Default']= dbuser
      data['Parameters']['InstanceType']['Default']= instance
      data['Parameters']['KeyName']['Default'] = key
      data['Parameters']['SSHLocation']['Default']= SSHloc
      
      client = boto3.client('cloudformation',
            region_name = 'ap-south-1',
            aws_access_key_id='ACCESS KEY',
            aws_secret_access_key='SECRET ACCESS KEY')
   
      client.create_stack(
         StackName= stackname,
         TemplateBody=json.dumps(data),
         DisableRollback=False,
         TimeoutInMinutes=1000
      )

      client.get_waiter('stack_create_complete').wait(StackName=stackname)
      cloudformation = boto3.resource('cloudformation',
            region_name = 'ap-south-1',
            aws_access_key_id='ACCESS KEY',
            aws_secret_access_key='SECRET ACCESS KEY')
      stack = cloudformation.Stack(stackname).outputs[0]
      url = stack["OutputValue"]
      webbrowser.open(url)
      
      
      return render_template("next.html") 

   
            

   return render_template("UI.html") 


if __name__ == '__main__':
   app.run()