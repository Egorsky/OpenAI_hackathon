# Agent Factor
This project is made in 24+ hours during OpenAI hackaton in Warsaw, Poland. The project uses agents to help manage users crypto assets and prevent from him from sending assets to fradulent wallets.

- Fetches data from Aave V3 account from Base chain.
- Assistent can check whether crypto wallet to which user want to make transaction is fradulent or not.
- Can do a web search in regards to crypto currencies.

# Tech stack

## Frontend
Frontend is fully made with Lovable <img src="https://github.com/user-attachments/assets/ce24933b-5c1a-41d2-aa1a-c527f15d11b3"
     alt="my-icon"
     width="20">
. It sonsists of:

- React with TypeScript
- Vite for build tooling
- TailwindCSS for styling
- shadcn/ui for UI components
- next-themes for dark/light mode
- React Query for data fetching

## Backend
- FastAPI for the REST API
- Uvicorn for ASGI server
- OpenAI API integration
- Zep for memory management

## Blockchain Integration
- Aave V3 protocol integration
- Base chain connectivity

## Infrastructure
- CORS middleware for API security
- Environment variables management
- Hot reload for development

## Development Tools
- Node.js & npm for package management
- Python 3.11+ for backend runtime

## Project Structure
```
project/
├── frontend/          # React + TypeScript frontend
├── src/             # Core source code
    ├── api         # Folder with FastAPI functionality
        ├── app.py  # FastAPI backend
│   ├── agent.py    # Agent implementation
└── tools/          # Agent tools implementation
    ├── aave.py     # Aave integration
    └── fraud.py    # Fraud detection
    └── web_search.py    # Blockchain web search with guardrails
    └── search_memory.py    # Memory tool
```

# Getting Started

## Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key
- Zep API key
- Ethereum wallet (MetaMask recommended)

## Installation

### Backend Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/agent-factor.git
cd agent-factor

# Create and activate virtual environment
make env

# Install dependencies
make install

# Create .env file
copy .env.example .env
# Add your API keys to .env file
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create frontend environment file
copy .env.example .env.local
```

## Running the Application

### Start Backend
```bash
# From project root with venv activated
make app
```
Backend will start at http://localhost:8000

### Start Frontend
```bash
# In a new terminal, from frontend directory
cd frontend
npm run dev
```
Frontend will start at http://localhost:5173

# Features
- 🤖 Memory tool
- 🔒 Fraud detection for wallet addresses
- 📊 Aave V3 integration for DeFi insights
- 🌐 Web search capabilities for crypto information
- 🌙 Dark/Medieval mode support

# Contributing
This project was created during the OpenAI hackathon in Warsaw, Poland. Feel free to submit issues and enhancement requests.
