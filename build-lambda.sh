#!/bin/bash

# Clean up existing build directory
rm -rf build
mkdir -p build/python

pip install -r requirements.txt -t build/python

# Copy Python files and directories
cp -r *.py models services main.py build/python/

cd build/python

zip -r9 ../function.zip .

S3_BUCKET="${S3_BUCKET}"
S3_PATH="nairobi-gems/lambda-zips/"

# Upload the zip to S3
aws s3 cp ../function.zip s3://$S3_BUCKET/$S3_PATH

cd ../..

echo "✅ Lambda package uploaded to S3 at s3://$S3_BUCKET/$S3_PATH"
