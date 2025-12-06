# **Terraform Installation Runbook (Ubuntu 24.04)**

## **1. Install Required Packages**

```bash
sudo apt install software-properties-common gnupg2 -y
```

## **2. Add HashiCorp GPG Key**

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
```

## **3. Add HashiCorp APT Repository**

```bash
sudo apt-add-repository "deb [arch=$(dpkg --print-architecture)] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

## **4. Update Package Index**

```bash
sudo apt update
```

## **5. Install Terraform**

```bash
sudo apt install terraform -y
```

## **6. Verify Installation**

```bash
terraform --version
```
