# 🗳️ Vote Chori Prevention DApp

A blockchain-based **secure online voting system** that prevents duplicate votes and ensures transparency using **Ethereum Smart Contracts**, **Web3.js**, and **MetaMask**.  
Voters verify their identity via **OTP** before accessing the blockchain voting portal.

---

## 🚀 Features

- 🔐 OTP-based voter verification (Aadhaar + Email)
- 🦊 MetaMask wallet integration
- 🗳️ Blockchain-powered voting (Ethereum)
- 📊 Real-time vote count display
- 🚫 Prevention of duplicate voting
- 🎨 Classy gradient UI design with smooth animations

---

## 🧠 Tech Stack

| Component | Technology |
|------------|-------------|
| Smart Contract | Solidity |
| Blockchain Interaction | Web3.js |
| Frontend | HTML, CSS, JavaScript |
| Backend | Flask (Python) |
| Database | SQLite |
| Wallet | MetaMask |
| Network | Ethereum (Testnet) |

---

## ⚙️ Setup Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/vote-chori-prevention.git
   cd vote-chori-prevention
   ```

2. **Install backend dependencies**
   ```bash
   pip install flask web3 flask-cors
   ```

3. **Deploy Smart Contract**
   - Open [Remix IDE](https://remix.ethereum.org)
   - Paste the Solidity code from `contracts/VoteChoriPrevention.sol`
   - Compile and deploy to your preferred Ethereum test network
   - Copy your **contract address** and **ABI**

4. **Connect Frontend**
   - Add the contract address inside `script.js`
   - Save the ABI JSON in `/static/abi.json`

5. **Run Flask App**
   ```bash
   python app.py
   ```

6. **Access on Browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 🧾 How It Works

1. User enters **Aadhaar** and **Email** → OTP sent  
2. User verifies OTP → access granted  
3. Connect **MetaMask wallet**  
4. Parties load dynamically from blockchain  
5. User casts a vote → recorded on blockchain  
6. Duplicate voting automatically restricted  

---

## 🪪 Party Images (Example)

| Logo | Party Name |
|------|-------------|
| 🟧 BJP | Bharatiya Janata Party |
| 🟩 AAP | Aam Aadmi Party |
| 🟦 INC | Indian National Congress |

---

## 🧰 Future Enhancements

- 🧾 Admin dashboard to view total votes  
- 🌐 IPFS-based voter record storage  
- 💠 Polygon / Sepolia Testnet deployment  
- 📱 QR-based voter verification  

---

## 👨‍💻 Author

**Ritesh Honule**  
📍 Belgaum, Karnataka, India  
🎓 MCA Student | Blockchain & Full Stack Developer  
🌐 Portfolio: *[Add your portfolio link]*  
📧 Email: *[Add your email]*  

---

## 📜 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

### ✨ “Empowering Democracy through Blockchain Transparency.” ✨

