// ==============================
// 🗳️ Vote Chori Prevention DApp
// ==============================

// Global variables
let web3;
let contract;
let userAccount;

// Your deployed smart contract address (replace with your actual one)
const contractAddress = "0x192cAC1D5e9f4ef35DAd644A88C501AF3774E4C7";

// ABI file loaded dynamically from static folder
fetch("/templates/abi.json")
  .then((res) => res.json())
  .then((abi) => {
    contractABI = abi;
    console.log("✅ ABI loaded successfully");
  })
  .catch((err) => console.error("❌ Failed to load ABI:", err));

// -----------------------------
// 1️⃣ Aadhaar + Email Submission
// -----------------------------
async function sendOTP() {
  const aadhaar = document.getElementById("aadhaar").value.trim();
  const email = document.getElementById("email").value.trim();

  if (aadhaar.length !== 12 || isNaN(aadhaar)) {
    alert("Enter a valid 12-digit Aadhaar number!");
    return;
  }
  if (!email.includes("@")) {
    alert("Enter a valid email!");
    return;
  }

  try {
    const response = await fetch("/send_otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ aadhaar, email }),
    });

    const data = await response.json();
    if (data.success) {
      alert("✅ OTP sent to your email!");
      window.location.href = "/otp";
    } else {
      alert("❌ Failed to send OTP. Try again.");
    }
  } catch (err) {
    console.error(err);
  }
}

// -----------------------------
// 2️⃣ OTP Verification
// -----------------------------
async function verifyOTP() {
  const otp = document.getElementById("otp").value.trim();
  try {
    const response = await fetch("/verify_otp", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ otp }),
    });
    const data = await response.json();
    if (data.success) {
      alert("✅ OTP Verified Successfully!");
      window.location.href = "/wallet";
    } else {
      alert("❌ Invalid OTP. Try again.");
    }
  } catch (err) {
    console.error(err);
  }
}

// -----------------------------
// 3️⃣ Connect Wallet (MetaMask)
// -----------------------------
async function connectWallet() {
  if (window.ethereum) {
    try {
      web3 = new Web3(window.ethereum);
      await window.ethereum.request({ method: "eth_requestAccounts" });
      const accounts = await web3.eth.getAccounts();
      userAccount = accounts[0];
      document.getElementById("walletAddress").innerText =
        "Connected: " + userAccount;
      await loadContract();
    } catch (err) {
      console.error("Wallet connection failed:", err);
      alert("⚠️ Please connect MetaMask properly.");
    }
  } else {
    alert("❌ MetaMask not installed!");
  }
}

// -----------------------------
// 4️⃣ Load Smart Contract
// -----------------------------
async function loadContract() {
  try {
    contract = new web3.eth.Contract(contractABI, contractAddress);
    console.log("✅ Smart contract connected");
    loadParties();
  } catch (err) {
    console.error("❌ Failed to load contract:", err);
  }
}

// -----------------------------
// 5️⃣ Load Political Parties
// -----------------------------
async function loadParties() {
  try {
    const parties = await contract.methods.getAllVotes().call();
    const container = document.getElementById("partiesContainer");
    container.innerHTML = "";

    parties.forEach((party, index) => {
      const card = document.createElement("div");
      card.className = "party-card";
      card.innerHTML = `
        <h2>${party.name}</h2>
        <p>Votes: ${party.votes}</p>
        <button id="voteBtn${index}" class="vote-btn" onclick="vote(${index}, '${party.name}')">Vote</button>
      `;
      container.appendChild(card);
    });
  } catch (error) {
    console.error("⚠️ Failed to load parties. Check contract or ABI.", error);
  }
}

// -----------------------------
// 6️⃣ Voting Functionality
// -----------------------------
window.vote = async (index, partyName) => {
  try {
    const hasVoted = await contract.methods.voters(userAccount).call();
    if (hasVoted) {
      alert("⚠️ You have already voted!");
      return;
    }

    await contract.methods.vote(index).send({ from: userAccount });
    document.getElementById(
      "resultMessage"
    ).innerText = `✅ You voted for ${partyName}`;
    disableAllButtons();
    loadParties();

    // Save vote to backend database
    await fetch("/save_vote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: userAccount, party: partyName }),
    });
  } catch (error) {
    console.error("❌ Voting error:", error);
    alert("Transaction failed or canceled.");
  }
};

// -----------------------------
// 7️⃣ Disable all vote buttons
// -----------------------------
function disableAllButtons() {
  const buttons = document.querySelectorAll(".vote-btn");
  buttons.forEach((btn) => {
    btn.disabled = true;
    btn.style.opacity = "0.5";
    btn.innerText = "Voted";
  });
}

// -----------------------------
// 8️⃣ Utility Event Bindings
// -----------------------------
document.addEventListener("DOMContentLoaded", () => {
  const sendOtpBtn = document.getElementById("sendOtpBtn");
  if (sendOtpBtn) sendOtpBtn.addEventListener("click", sendOTP);

  const verifyOtpBtn = document.getElementById("verifyOtpBtn");
  if (verifyOtpBtn) verifyOtpBtn.addEventListener("click", verifyOTP);

  const connectWalletBtn = document.getElementById("connectWalletBtn");
  if (connectWalletBtn)
    connectWalletBtn.addEventListener("click", connectWallet);
});

console.log("✅ script.js loaded successfully");
