# Declares inputs accepted by the Terraform configuration.
# Terraform automatically maps TF_VAR_subscription_id (from env of cicd.yml) -> var.subscription_id

variable "subscription_id" {
  description = "Azure subscription ID."
  type        = string
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "canadaeast"
}

variable "environment" {
  description = "Environment name."
  type        = string
  default     = "dev"
}

variable "name_prefix" {
  description = "Prefix used in resource names."
  type        = string
  default     = "spacebnb"
}

variable "github_actions_principal_id" {
  description = "Object ID of the GitHub Actions service principal."
  type        = string
}