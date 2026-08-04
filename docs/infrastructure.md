# Foundational Resources

This project uses three foundational technologies:

- **Terraform** (`/infrastructure`)
  - Provisions and manages Azure infrastructure.
  - Examples: Resource Groups, VNets, AKS, Azure Container Registry, Log Analytics Workspace, Managed Identities.

- **Kubernetes** (`/deployment`)
  - Manages workloads running inside the AKS cluster.
  - Examples: Deployments, Services, Ingress, ConfigMaps, Secrets.

- **GitHub Actions** (`/.github/workflows`)
  - Orchestrates CI/CD workflows.
  - Detects changes to the repository and executes Terraform and Kubernetes commands when appropriate.

---

# Prerequisites

## 1. GitHub Actions Identity

GitHub Actions authenticates to Azure using a Microsoft Entra Service Principal (OIDC).

Recommended Azure roles:

- Contributor
- Role Based Access Control Administrator

These permissions allow the workflow to:

- Provision Azure resources
- Create Azure role assignments (e.g. `AcrPull`)

---

## 2. Terraform Remote State

Terraform requires a remote backend before it can initialize.

The backend consists of:

- Resource Group
- Storage Account
- Blob Container

The CI/CD pipeline ensures these resources exist before executing `terraform init`.

This bootstrap step is idempotent:

- Create the Resource Group if missing.
- Create the Storage Account if missing.
- Create the Blob Container if missing.
- Continue with Terraform initialization.

> **Note**
>
> If the `Microsoft.Storage` resource provider is not registered, Storage Account creation may fail with a misleading `SubscriptionNotFound` error.

---
---

# 1. Configure GitHub Actions

Create the GitHub Actions workflow under:

```
.github/workflows/
```

Responsibilities:

- Authenticate to Azure
- Ensure the Terraform backend exists
- Run Terraform commands
- Build container images (when application code changes)
- Push images to ACR
- Deploy Kubernetes manifests

---

# 2. Define Infrastructure (Terraform)

Terraform configuration lives in:

```
/infrastructure
```

Minimum structure:

- `versions.tf`
  - Which Terraform and provider versions are required?

- `backend.tf`
  - Where should Terraform store its state?

- `providers.tf`
  - Which cloud provider(s) should Terraform use?

- `variables.tf`
  - What deployment inputs are configurable?

- `main.tf`
  - Which Azure resources should exist?

- `outputs.tf`
  - Which values should be exposed to other tools or pipelines?

---

# 3. Define Kubernetes Resources

Kubernetes manifests live in:

```
/deployment
```

Minimum structure:

- `ingress.yaml`
  - External entry point into the cluster.

Each microservice:

```
auth/
    deployment.yaml
    service.yaml
    configmap.yaml

listing/
    deployment.yaml
    service.yaml

reservation/
    deployment.yaml
    service.yaml
```

Responsibilities:

- Deploy Pods
- Expose Services
- Configure application settings
- Route external traffic

---

# Overall Deployment Flow

```
Developer pushes changes
            │
            ▼
GitHub Actions
            │
            ├── Ensure Terraform backend exists
            │
            ├── terraform init
            ├── terraform validate
            ├── terraform plan
            ├── terraform apply
            │
            ├── Build container images (if needed)
            ├── Push images to ACR
            │
            └── kubectl apply
                    │
                    ▼
            Kubernetes reconciles workloads
```