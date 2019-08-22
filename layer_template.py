#!/usr/bin/env python
"""
Script to create a new Lambda Layer CFN template via Troposphere
"""

from datetime import datetime
import argparse
from troposphere import (
    Parameter,
    Template,
    GetAtt,
    Sub,
    Ref
)
from troposphere.awslambda import (
    LayerVersion, Content
)
VERSION = datetime.utcnow().isoformat()

TEMPLATE = Template()
TEMPLATE.set_description(f'Template to create a Lambda layer. Version {VERSION}')

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '--runtimes', action='append', required=True
)
PARSER.add_argument(
    '--s3-bucket', required=True
)
PARSER.add_argument(
    '--s3-key', required=True
)
PARSER.add_argument(
    '--json', action='store_true'
)

ARGS = PARSER.parse_args()

LAYER_NAME = TEMPLATE.add_parameter(Parameter(
    'LayerName',
    Type="String",
    AllowedPattern='[a-z]+'
))

LAYER = TEMPLATE.add_resource(LayerVersion(
    'LayerVersion',
    CompatibleRuntimes=ARGS.runtimes,
    Description=Sub(f'Layer ${{{LAYER_NAME.title}}}'),
    LayerName=Ref(LAYER_NAME),
    Content=Content(
        S3Bucket=ARGS.s3_bucket,
        S3Key=ARGS.s3_key
    )
))
if ARGS.json:
    print(TEMPLATE.to_json())
else:
    print(TEMPLATE.to_yaml())
