#!/usr/bin/env node

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Find the Python executable in the virtual environment
const projectRoot = join(__dirname, '..');
const venvPython = process.platform === 'win32' 
  ? join(projectRoot, 'venv', 'Scripts', 'python.exe')
  : join(projectRoot, 'venv', 'bin', 'python');

const setupScript = join(projectRoot, 'setup_auth.py');

console.log('🔧 Starting Substack MCP Plus authentication setup...\n');

// Spawn the Python setup script
const setupProcess = spawn(venvPython, [setupScript], {
  stdio: 'inherit',
  cwd: projectRoot
});

setupProcess.on('error', (err) => {
  console.error('❌ Failed to start setup:', err.message);
  console.error('💡 Try running: python setup_auth.py');
  process.exit(1);
});

setupProcess.on('exit', (code) => {
  if (code === 0) {
    console.log('\n✅ Setup complete! Next steps:');
    console.log('1. Configure Claude Desktop (see docs)');
    console.log('2. Restart Claude Desktop');
    console.log('3. Start creating content!');
  }
  process.exit(code || 0);
});