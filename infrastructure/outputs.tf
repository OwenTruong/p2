# Declares values Terraform should expose after deployment.

output "resource_group_name" {
  description = "Name of the deployed resource group."
  value       = azurerm_resource_group.main.name
}

output "virtual_network_name" {
  description = "Name of the deployed virtual network."
  value       = azurerm_virtual_network.main.name
}