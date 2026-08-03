# Tells Terraform where the state for this configuration should be stored.
# The block is empty because the GitHub Actions workflow supplies the backend names during terraform init.

terraform {
  backend "azurerm" {}
}