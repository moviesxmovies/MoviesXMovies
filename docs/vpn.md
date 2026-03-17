---
icon: lucide/globe-lock
title: VPN
---

## Why Use a VPN?

Using a VPN provides an essential layer of `security`. It ensures that sensitive business data—such as administration panels, statistics, and internal documentation—cannot be accessed from outside the corporate network.

---

## How to Set Up

### 1. Install WireGuard

Follow the installation steps corresponding to your operating system on the [official WireGuard website](https://www.wireguard.com/install/).

### 2. Set Up Keys

You need to generate a public and private key pair to authenticate your connection. Run the following commands in your terminal:

!!! note "Generate Private Key"
    ```bash
    wg genkey | tee ~/wireguard_private.key
    ```

!!! note "Generate Public Key"
    ```bash
    wg pubkey < ~/wireguard_private.key | tee ~/wireguard_public.key
    ```

### 3. Create the Interface

Create your WireGuard configuration file and paste the following snippet. Make sure to replace the placeholder variables with your actual keys and assigned IP address.

```bash title="/etc/wireguard/wg0.conf"
[Interface]
Address = 10.0.0.3/24  # <- Your assigned VPN IP (provided by the administrator)
PrivateKey = <CLIENT_PRIVATE_KEY> # <- Your private key
DNS = 1.1.1.1

[Peer]
PublicKey = <SERVER_PUBLIC_KEY> # <- Server public key
Endpoint = ssh.moviesxmovies.jonaykb.com:51820
AllowedIPs = 10.0.0.0/24
```

### 4. Request Access

Next, you must contact [supply@moviesxmovies.jonaykb.com](mailto:supply@moviesxmovies.jonaykb.com) to get your public key whitelisted. Please include the following information in your email:

!!! warning "Required Information via Email"
**Subject:** `<FULL_NAME> - VPN ACCESS`

**Description:**
```
`<CLIENT_PUBLIC_KEY>`
`<GITHUB_USERNAME>`
```

### 5. Connect and Verify

Once your setup is complete and access is granted, bring up the interface to connect:

```bash
sudo wg-quick up wg0
```

To verify that the connection was successful, check your WireGuard status:

```bash
sudo wg show
```

> **Success Check:** You should now be able to reach internal services (for example, Grafana at [10.0.0.1:3000](https://www.google.com/search?q=http://10.0.0.1:3000)). Additionally, the output of `sudo wg show` should display a `last handshake` line, confirming an active and healthy connection.
