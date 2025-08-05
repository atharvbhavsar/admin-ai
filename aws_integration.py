import boto3
import json
import logging
from typing import Optional, Dict, Any, List
from botocore.exceptions import NoCredentialsError, ClientError
from config import Config

logger = logging.getLogger(__name__)

class AWSManager:
    """Manages AWS services integration"""
    
    def __init__(self):
        self.aws_access_key = Config.AWS_ACCESS_KEY_ID
        self.aws_secret_key = Config.AWS_SECRET_ACCESS_KEY
        self.aws_region = Config.AWS_REGION
        
        # Initialize AWS clients
        self.session = None
        self.s3_client = None
        self.sns_client = None
        self.ses_client = None
        self.lambda_client = None
        self.dynamodb = None
        
        if Config.is_aws_configured():
            self._initialize_aws_clients()
    
    def _initialize_aws_clients(self):
        """Initialize AWS service clients"""
        try:
            self.session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            self.s3_client = self.session.client('s3')
            self.sns_client = self.session.client('sns')
            self.ses_client = self.session.client('ses')
            self.lambda_client = self.session.client('lambda')
            self.dynamodb = self.session.resource('dynamodb')
            
            logger.info("AWS clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing AWS clients: {e}")
    
    def upload_to_s3(self, file_content: bytes, bucket_name: str, file_key: str, content_type: str = None) -> Optional[str]:
        """Upload file to S3 bucket"""
        if not self.s3_client:
            return None
        
        try:
            extra_args = {}
            if content_type:
                extra_args['ContentType'] = content_type
            
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=file_content,
                **extra_args
            )
            
            # Generate URL
            url = f"https://{bucket_name}.s3.{self.aws_region}.amazonaws.com/{file_key}"
            return url
            
        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            return None
    
    def send_email_notification(self, to_emails: List[str], subject: str, message: str, html_message: str = None) -> bool:
        """Send email notification using SES"""
        if not self.ses_client:
            return False
        
        try:
            destination = {'ToAddresses': to_emails}
            
            message_body = {'Text': {'Data': message}}
            if html_message:
                message_body['Html'] = {'Data': html_message}
            
            self.ses_client.send_email(
                Source='noreply@admitai.com',  # Replace with verified email
                Destination=destination,
                Message={
                    'Subject': {'Data': subject},
                    'Body': message_body
                }
            )
            
            return True
            
        except ClientError as e:
            logger.error(f"Error sending email via SES: {e}")
            return False
    
    def send_sms_notification(self, phone_number: str, message: str) -> bool:
        """Send SMS notification using SNS"""
        if not self.sns_client:
            return False
        
        try:
            self.sns_client.publish(
                PhoneNumber=phone_number,
                Message=message
            )
            
            return True
            
        except ClientError as e:
            logger.error(f"Error sending SMS via SNS: {e}")
            return False
    
    def invoke_lambda_function(self, function_name: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Invoke AWS Lambda function"""
        if not self.lambda_client:
            return None
        
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            if response['StatusCode'] == 200:
                result = json.loads(response['Payload'].read())
                return result
            else:
                logger.error(f"Lambda invocation failed with status: {response['StatusCode']}")
                return None
                
        except ClientError as e:
            logger.error(f"Error invoking Lambda function: {e}")
            return None
    
    def store_user_data(self, table_name: str, user_data: Dict[str, Any]) -> bool:
        """Store user data in DynamoDB"""
        if not self.dynamodb:
            return False
        
        try:
            table = self.dynamodb.Table(table_name)
            table.put_item(Item=user_data)
            return True
            
        except ClientError as e:
            logger.error(f"Error storing data in DynamoDB: {e}")
            return False
    
    def get_user_data(self, table_name: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data from DynamoDB"""
        if not self.dynamodb:
            return None
        
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(Key={'user_id': user_id})
            
            if 'Item' in response:
                return response['Item']
            else:
                return None
                
        except ClientError as e:
            logger.error(f"Error getting data from DynamoDB: {e}")
            return None
    
    def create_cloudformation_stack(self, stack_name: str, template_body: str, parameters: List[Dict[str, str]] = None) -> bool:
        """Create CloudFormation stack for infrastructure"""
        if not self.session:
            return False
        
        try:
            cloudformation = self.session.client('cloudformation')
            
            args = {
                'StackName': stack_name,
                'TemplateBody': template_body,
                'Capabilities': ['CAPABILITY_IAM']
            }
            
            if parameters:
                args['Parameters'] = parameters
            
            cloudformation.create_stack(**args)
            return True
            
        except ClientError as e:
            logger.error(f"Error creating CloudFormation stack: {e}")
            return False
    
    def get_deployment_template(self) -> str:
        """Get CloudFormation template for AdmitAI deployment"""
        
        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Description": "AdmitAI College Admission Platform Infrastructure",
            "Parameters": {
                "EnvironmentType": {
                    "Type": "String",
                    "Default": "development",
                    "AllowedValues": ["development", "staging", "production"]
                },
                "InstanceType": {
                    "Type": "String",
                    "Default": "t3.micro",
                    "AllowedValues": ["t3.micro", "t3.small", "t3.medium"]
                }
            },
            "Resources": {
                "AdmitAIVPC": {
                    "Type": "AWS::EC2::VPC",
                    "Properties": {
                        "CidrBlock": "10.0.0.0/16",
                        "EnableDnsHostnames": True,
                        "EnableDnsSupport": True,
                        "Tags": [{"Key": "Name", "Value": "AdmitAI-VPC"}]
                    }
                },
                "AdmitAISubnet": {
                    "Type": "AWS::EC2::Subnet",
                    "Properties": {
                        "VpcId": {"Ref": "AdmitAIVPC"},
                        "CidrBlock": "10.0.1.0/24",
                        "AvailabilityZone": {"Fn::Select": [0, {"Fn::GetAZs": ""}]},
                        "MapPublicIpOnLaunch": True,
                        "Tags": [{"Key": "Name", "Value": "AdmitAI-Subnet"}]
                    }
                },
                "AdmitAISecurityGroup": {
                    "Type": "AWS::EC2::SecurityGroup",
                    "Properties": {
                        "GroupDescription": "Security group for AdmitAI application",
                        "VpcId": {"Ref": "AdmitAIVPC"},
                        "SecurityGroupIngress": [
                            {
                                "IpProtocol": "tcp",
                                "FromPort": 80,
                                "ToPort": 80,
                                "CidrIp": "0.0.0.0/0"
                            },
                            {
                                "IpProtocol": "tcp",
                                "FromPort": 443,
                                "ToPort": 443,
                                "CidrIp": "0.0.0.0/0"
                            },
                            {
                                "IpProtocol": "tcp",
                                "FromPort": 22,
                                "ToPort": 22,
                                "CidrIp": "0.0.0.0/0"
                            }
                        ]
                    }
                },
                "AdmitAIInstance": {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "InstanceType": {"Ref": "InstanceType"},
                        "ImageId": "ami-0c55b159cbfafe1d0",  # Amazon Linux 2
                        "SubnetId": {"Ref": "AdmitAISubnet"},
                        "SecurityGroupIds": [{"Ref": "AdmitAISecurityGroup"}],
                        "UserData": {
                            "Fn::Base64": {
                                "Fn::Join": ["\n", [
                                    "#!/bin/bash",
                                    "yum update -y",
                                    "yum install -y python3 git nginx",
                                    "pip3 install flask gunicorn",
                                    "git clone https://github.com/atharvbhavsar/admin-ai.git /opt/admitai",
                                    "cd /opt/admitai",
                                    "pip3 install -r requirements.txt",
                                    "systemctl enable nginx",
                                    "systemctl start nginx"
                                ]]
                            }
                        },
                        "Tags": [{"Key": "Name", "Value": "AdmitAI-Server"}]
                    }
                },
                "AdmitAIS3Bucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "BucketName": {"Fn::Sub": "admitai-storage-${AWS::AccountId}"},
                        "PublicReadPolicy": False,
                        "VersioningConfiguration": {"Status": "Enabled"}
                    }
                },
                "AdmitAIDynamoDBTable": {
                    "Type": "AWS::DynamoDB::Table",
                    "Properties": {
                        "TableName": "AdmitAI-Users",
                        "AttributeDefinitions": [
                            {"AttributeName": "user_id", "AttributeType": "S"}
                        ],
                        "KeySchema": [
                            {"AttributeName": "user_id", "KeyType": "HASH"}
                        ],
                        "BillingMode": "PAY_PER_REQUEST"
                    }
                }
            },
            "Outputs": {
                "WebsiteURL": {
                    "Description": "URL of the AdmitAI website",
                    "Value": {"Fn::Sub": "http://${AdmitAIInstance.PublicDnsName}"}
                },
                "S3BucketName": {
                    "Description": "S3 bucket for file storage",
                    "Value": {"Ref": "AdmitAIS3Bucket"}
                }
            }
        }
        
        return json.dumps(template, indent=2)
    
    def deploy_to_aws(self, stack_name: str = "AdmitAI-Stack") -> bool:
        """Deploy AdmitAI to AWS using CloudFormation"""
        
        template = self.get_deployment_template()
        return self.create_cloudformation_stack(stack_name, template)
    
    def get_aws_status(self) -> Dict[str, Any]:
        """Get AWS integration status"""
        return {
            "aws_configured": Config.is_aws_configured(),
            "s3_available": bool(self.s3_client),
            "ses_available": bool(self.ses_client),
            "sns_available": bool(self.sns_client),
            "lambda_available": bool(self.lambda_client),
            "dynamodb_available": bool(self.dynamodb),
            "region": self.aws_region
        }

# Global instance
aws_manager = AWSManager()