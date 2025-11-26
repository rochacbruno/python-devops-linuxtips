import boto3

ec2 = boto3.client('ec2')

# Criar Security Group
sg = ec2.create_security_group(
    GroupName='web-server-sg',
    Description='Permite HTTP e SSH'
)
sg_id = sg['GroupId']

# Adicionar regras
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

print(f"Security Group criado: {sg_id}")
