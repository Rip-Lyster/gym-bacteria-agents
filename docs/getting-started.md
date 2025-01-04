# Getting Started

This guide will help you set up and run the Gym Bacteria Agents project locally.

## Prerequisites

### Python Setup
1. Install pyenv and pyenv-virtualenv
   ```bash
   # macOS
   brew install pyenv pyenv-virtualenv
   
   # Add to your shell configuration (.zshrc, .bashrc, etc.):
   eval "$(pyenv init -)"
   eval "$(pyenv virtualenv-init -)"
   ```

2. Install Python and create virtualenv
   ```bash
   pyenv install $(cat .python-version)
   pyenv virtualenv $(cat .python-version) gym-bacteria-env
   pyenv local gym-bacteria-env
   ```

### Node.js Setup
1. Install nvm (Node Version Manager)
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
   
   # Add to your shell configuration (.zshrc, .bashrc, etc.):
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
   ```

2. Install Node.js
   ```bash
   nvm install 18.16.1
   nvm use 18.16.1
   ```

## Project Setup

1. Install dependencies
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node dependencies
   npm install
   ```

## Development

Run the development server with a single command:
```bash
npm run dev
```

This will start both:
- Next.js frontend on [http://localhost:3000](http://localhost:3000)
- Flask backend on [http://localhost:5328](http://localhost:5328)

## Production

Build and start the production server:
```bash
npm run build
npm start
```

## Troubleshooting

### Node Version
The project is configured to use Node.js v18.16.1. If you're using a different version, you might encounter compatibility issues. To switch to the correct version:
```bash
nvm use 18.16.1
npm install  # reinstall dependencies with the correct Node version
```

### NPM Vulnerabilities
If you see npm vulnerability warnings during installation, you can try to fix them with:
```bash
npm audit fix
```

For more aggressive fixes (may include breaking changes):
```bash
npm audit fix --force
```

### Verifying Installation
You can verify your installation by checking the versions:
```bash
# Check Node.js and npm versions
node -v  # Should be v18.16.1
npm -v

# Check Python and pip versions
python --version  # Should be Python 3.12.8 or compatible
pip --version
``` 