# Gym Bacteria Agents

A web application that combines Next.js for the frontend and Flask for the backend API.

## Quick Start

1. Setup Python environment (requires pyenv):
   ```bash
   pyenv install $(cat .python-version)
   pyenv virtualenv $(cat .python-version) gym-bacteria-env
   pyenv local gym-bacteria-env
   ```

2. Setup Node.js (requires nvm):
   ```bash
   nvm use
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

4. Start development servers:
   ```bash
   npm run dev
   ```

## Documentation

Detailed documentation can be found in the [`/docs`](docs) directory:

- [Getting Started Guide](docs/getting-started.md)
- [API Reference](docs/api-reference.md)
- [Development Guide](docs/development.md)
- [Architecture](docs/architecture.md)

## Project Structure
```
.
├── api/            # Flask backend
├── app/            # Next.js frontend
├── docs/           # Documentation
├── .nvmrc         # Node.js version specification
├── .python-version # Python version specification
├── requirements.txt # Python dependencies
└── package.json    # Node.js dependencies and scripts
```
