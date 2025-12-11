# Setup Ansible

## **1. Install system prerequisites**

```bash
sudo dnf install -y python3-pip python3-virtualenv python3-venv git
```

---

## **2. Install pipx**

```bash
python3 -m pip install --user pipx
~/.local/bin/pipx ensurepath
source ~/.bashrc
```

---

## **3. Install Python 3.9**

```bash
sudo dnf module install python39 -y
python3.9 --version
```

---

## **4. Install Ansible using Python 3.9**

```bash
pipx install --python python3.9 ansible --include-deps
ansible --version
```

---

## **5. Install OCI Ansible Collection**

```bash
ansible-galaxy collection install oracle.oci
ansible-doc -l | grep oracle.oci
```

---

## **6. Inject OCI SDK + required Python libraries into Ansible**

```bash
pipx inject ansible oci
pipx inject ansible cryptography requests
```

---

## **7. Verify**

```bash
pipx list
ansible --version
```

---

## Run Playbooks
```
ansible-playbook -i inventory.ini install_uma.yml
```