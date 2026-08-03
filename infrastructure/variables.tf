# Declares inputs accepted by the Terraform configuration.
# Terraform automatically maps TF_VAR_subscription_id (from env of cicd.yml) -> var.subscription_id

variable "subscription_id" {
  description = "Azure subscription where resources are deployed."
  type        = string
}

variable "location" {
  description = "Azure deployment region."
  type        = string
  default     = "canadaeast"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}