# The provider is the component that translates Terraform resources into Azure Resource Manager API operations

provider "azurerm" {
  features {}

  subscription_id = var.subscription_id
}