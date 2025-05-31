terraform {
  backend "s3" {
    bucket         = "bmdev-side-quests"
    key            = "nairobi-gems/terraform-state/terraform.tfstate"
    region         = "eu-west-1"
    dynamodb_table = "nairobi-gems-terraform-state"
    encrypt        = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# IAM Role for Lambda
resource "aws_iam_role" "nairobi-gems-lambda_role" {
  name = "nairobi-gems-lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
  lifecycle {
    create_before_destroy = true
    prevent_destroy = false
    ignore_changes = [
      name,
      assume_role_policy,
    ]
  }
}

# Lambda IAM Policy
resource "aws_iam_role_policy_attachment" "nairobi-gems-lambda_basic" {
  role       = aws_iam_role.nairobi-gems-lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Add CloudWatch Logs permissions
resource "aws_iam_role_policy" "lambda_logs" {
  name = "lambda-logs-policy"
  role = aws_iam_role.nairobi-gems-lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:FilterLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

# Lambda Function
resource "aws_lambda_function" "nairobi-gems-lambda" {
  function_name = var.app_name
  role          = aws_iam_role.nairobi-gems-lambda_role.arn
  handler       = "main.handler"
  runtime       = "python3.9"
  s3_bucket     = var.s3_bucket_name
  s3_key        = "nairobi-gems/lambda-zips/function.zip"
  source_code_hash = filebase64sha256("../build/function.zip")
  timeout       = 300
  memory_size   = 512

  environment {
    variables = {
      STAGE = "prod"
      GEMINI_API_KEY       = var.gemini_api_key
      GEMINI_MODEL         = var.gemini_model
      CURRENT_LLM_ENGINE   = var.current_llm_engine
    }
  }
}


