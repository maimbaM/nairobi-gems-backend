variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-1"
}

variable "gemini_api_key" {
  description = "Google Gemini API key"
  type        = string
  sensitive   = true
}

variable "gemini_model" {
  description = "Google Gemini model name"
  type        = string
  default     = "gemini-2.5-flash-preview-04-17"
}

variable "current_llm_engine" {
  description = "Current LLM engine to use"
  type        = string
  default     = "gemini"
}

variable "app_name" {
  description = "Name of the application"
  type        = string
  default     = "nairobi-gems-backend"
}

variable "s3_bucket_name" {
  description = "S3 bucket for storing lambda zipped function"
  type = string
}

variable "dynamo_table_name" {
  description = "dynamo table for storing terraform state"
  type = string
}

variable "environment" {
  description = "Environment for the application"
  type        = string
  default     = "prod"
}