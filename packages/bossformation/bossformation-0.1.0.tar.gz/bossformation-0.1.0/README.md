# bossformation

[![Build Status](https://travis-ci.org/cloudboss/bossformation.svg?branch=master)](https://travis-ci.org/cloudboss/bossformation)

`bossformation` is a preprocessor that allows [CloudFormation](https://aws.amazon.com/cloudformation/) templates to be written in YAML instead of JSON. In addition to this, templates may contain [Jinja2](http://jinja.pocoo.org/docs/dev/) tags, allowing for dynamic template generation.

# Installation
## Install from [PyPI](https://pypi.python.org/pypi)
```
pip install bossformation
```
## Install from source
```
git clone https://github.com/cloudboss/bossformation.git
cd bossformation
pip install -r requirements.txt
pip install .
```

# Usage
After installation, the `bf` command is provided with subcommand `render`.

## Rendering templates
At its simplest, you may write a CloudFormation template that maps YAML to JSON, such as the following file `test.yml`:

```
# The date must be quoted or the YAML parser will try to convert it to a datetime object
AWSTemplateFormatVersion: '2010-09-09'

Description: CloudFormation Example

Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: My group description
      SecurityGroupIngress:
        - SourceSecurityGroupId: sg-00000000
          IpProtocol: TCP
          FromPort: 443
          ToPort: 443
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: us-east-1a
      SecurityGroupIds:
        - Ref: MySecurityGroup
      ImageId: ami-00000000
```

Then run `render` on it (`-P` tells it to pretty-print the output).

```
bf render -t test.yml -P
```

The resulting output would be:

```
{
  "AWSTemplateFormatVersion": "2010-09-09",
  "Description": "CloudFormation Example",
  "Resources": {
    "MySecurityGroup": {
      "Type": "AWS::EC2::SecurityGroup",
      "Properties": {
        "SecurityGroupIngress": [
          {
            "SourceSecurityGroupId": "sg-00000000",
            "IpProtocol": "TCP",
            "ToPort": 443,
            "FromPort": 443
          }
        ],
        "GroupDescription": "My group description"
      }
    },
    "MyInstance": {
      "Type": "AWS::EC2::Instance",
      "Properties": {
        "AvailabilityZone": "us-east-1a",
        "SecurityGroupIds": [
          {
            "Ref": "MySecurityGroup"
          }
        ],
        "ImageId": "ami-00000000"
      }
    }
  }
}
```

## Adding Properties
At this point, you may want to change the template so that it is region-agnostic. To do this, you can provide properties in a separate file that will be available within the template.

Create a file `properties.yml`:

```
AvailabilityZone: us-east-1a
SuperSecurityGroup: sg-00000001
```

Then modify the original template to include the properties within Jinja2 tags.

```
# The date must be quoted or the YAML parser will try to convert it to a datetime object
AWSTemplateFormatVersion: '2010-09-09'

Description: CloudFormation Example

Resources:
  MySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: My group description
      SecurityGroupIngress:
        - SourceSecurityGroupId: sg-00000000
          IpProtocol: TCP
          FromPort: 443
          ToPort: 443
  MyInstance:
    Type: AWS::EC2::Instance
    Properties:
      AvailabilityZone: {{ AvailabilityZone }}
      SecurityGroupIds:
        - {{ SuperSecurityGroup }}
        - Ref: MySecurityGroup
      ImageId: ami-00000000
```

Run `render` again, passing the path to the properties file with `-p`:

```
bf render -p properties.yml -t test.yml -P
```

## Dynamic Properties
Templates themselves are meant to be stateless. That is, if the properties passed into a template are the same, then the rendered output should be the same. However, properties files may contain dynamic lookups into AWS, which are enabled by a Jinja2 context that is passed to the properties.

If you use this feature, you must authenticate to AWS and provide a region:
```
export AWS_PROFILE=heavyk
export AWS_DEFAULT_REGION=us-east-1
```

Now you may include dynamic lookups within `properties.yml`:
```
AvailabilityZones: {{ azs() }}
AmiId: {{ ami_id_for('amzn-ami-hvm-2015.09.2.x86_64-gp2') }}
```

Properties files have the following functions available within their Jinja2 context:

* `azs()`:

 Returns a list of the availability zones for the current region.

* `ami_id_for(name)`:

 Returns the AMI ID for the given AMI name. If `name` is an AMI ID, then it is returned verbatim.

* `sg_id_for(name)`:

 Returns the security group ID for the given security group name. If `name` is a security group ID, then it is returned verbatim.

* `subnet_id_for(name)`:

 Returns the subnet ID for the given subnet name. If `name` is a subnet ID, then it is returned verbatim.

### Authenticating with AWS
`bossformation` uses standard AWS SDK environment variables for authentication, which are described in the [boto3 documentation](http://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration).

The simplest way to authenticate if you are not running `bossformation` on an EC2 instance is to configure `~/.aws/credentials` with a [profile](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-multiple-profiles) and pass its name in the environment variable `AWS_PROFILE`.

If you are running `bossformation` on an EC2 instance, you may assign the instance an [IAM role](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) upon creation, and then you do not need to pass any credentials. The following IAM policy may be applied to the role, and will enable "describe" access for all EC2 resources. If you wish, you may further limit the policy by explicitly allowing or denying specific resources.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:Describe*"
            ],
            "Resource": "*"
        }
    ]
}
```

### Region
You must set the AWS region you are running in. To do this, set the `AWS_DEFAULT_REGION` environment variable.
