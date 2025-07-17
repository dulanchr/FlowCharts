// script.js
class FlowchartConverter {
    constructor() {
        this.initializeElements();
        this.attachEventListeners();
        this.currentFlowchartData = null;
    }

    initializeElements() {
        this.codeInput = document.getElementById('codeInput');
        this.generateBtn = document.getElementById('generateBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.fontSizeInput = document.getElementById('fontSize');
        this.flowchartOutput = document.getElementById('flowchartOutput');
        this.loadingIndicator = document.getElementById('loadingIndicator');
        this.errorMessage = document.getElementById('errorMessage');
        this.errorText = document.getElementById('errorText');
    }

    attachEventListeners() {
        this.generateBtn.addEventListener('click', () => this.generateFlowchart());
        this.downloadBtn.addEventListener('click', () => this.downloadFlowchart());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        
        // Allow Enter key to generate (with Ctrl/Cmd modifier)
        this.codeInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.generateFlowchart();
            }
        });
        
        // Auto-resize textarea
        this.codeInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    autoResizeTextarea() {
        const textarea = this.codeInput;
        textarea.style.height = 'auto';
        textarea.style.height = Math.max(300, textarea.scrollHeight) + 'px';
    }

    async generateFlowchart() {
        const pseudocode = this.codeInput.value.trim();
        const fontSize = parseInt(this.fontSizeInput.value) || 20;

        if (!pseudocode) {
            this.showError('Please enter some pseudocode');
            return;
        }

        this.showLoading();
        this.hideError();

        try {
            // Simulate API call - In real implementation, this would call your Flask backend
            const response = await this.callFlowchartAPI(pseudocode, fontSize);
            
            if (response.success) {
                this.displayFlowchart(response.imageData, response.filename);
            } else {
                this.showError(response.error || 'Failed to generate flowchart');
            }
        } catch (error) {
            console.error('Error generating flowchart:', error);
            this.showError('Network error occurred. Please try again.');
        } finally {
            this.hideLoading();
        }
    }

    async callFlowchartAPI(pseudocode, fontSize) {
        // This is a mock implementation
        // In real implementation, you would call your Flask backend:
        // const response = await fetch('/generate-flowchart', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({
        //         pseudocode: pseudocode,
        //         fontSize: fontSize
        //     })
        // });
        // return await response.json();

        // Mock response for demonstration
        return new Promise((resolve) => {
            setTimeout(() => {
                // Simulate successful response
                resolve({
                    success: true,
                    imageData: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjhmOWZhIi8+CiAgPGNpcmNsZSBjeD0iMjAwIiBjeT0iNDAiIHI9IjMwIiBmaWxsPSJub25lIiBzdHJva2U9IiMzMzMiIHN0cm9rZS13aWR0aD0iMiIvPgogIDx0ZXh0IHg9IjIwMCIgeT0iNDUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzMzMyI+U1RBUlQ8L3RleHQ+CiAgPGxpbmUgeDE9IjIwMCIgeTE9IjcwIiB4Mj0iMjAwIiB5Mj0iMTAwIiBzdHJva2U9IiMzMzMiIHN0cm9rZS13aWR0aD0iMiIvPgogIDxwb2x5Z29uIHBvaW50cz0iMTUwLDEwMCAyNTAsMTAwIDI3MCwxMzAgMjMwLDE2MCAyNTAsMTkwIDE1MCwxOTAgMTMwLDE2MCAyNTAsMTMwIiBmaWxsPSJub25lIiBzdHJva2U9IiMzMzMiIHN0cm9rZS13aWR0aD0iMiIvPgogIDx0ZXh0IHg9IjIwMCIgeT0iMTQ1IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9IiMzMzMiPk1vY2sgRmxvd2NoYXJ0PC90ZXh0PgogIDx0ZXh0IHg9IjIwMCIgeT0iMjIwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTAiIGZpbGw9IiM2NjYiPkNvbm5lY3QgdG8gRmxhc2sgYmFja2VuZCBmb3IgcmVhbCBmbG93Y2hhcnRzPC90ZXh0Pgo8L3N2Zz4=',
                    filename: 'flowchart.png'
                });
            }, 1500);
        });
    }

    displayFlowchart(imageData, filename) {
        this.currentFlowchartData = { imageData, filename };
        
        this.flowchartOutput.innerHTML = `
            <img src="${imageData}" alt="Generated Flowchart" />
        `;
        
        this.downloadBtn.disabled = false;
    }

    downloadFlowchart() {
        if (!this.currentFlowchartData) return;

        const { imageData, filename } = this.currentFlowchartData;
        
        // Create download link
        const link = document.createElement('a');
        link.href = imageData;
        link.download = filename || 'flowchart.png';
        
        // Trigger download
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    clearAll() {
        this.codeInput.value = '';
        this.flowchartOutput.innerHTML = `
            <div class="placeholder">
                <div class="placeholder-icon">📊</div>
                <h3>Your flowchart will appear here</h3>
                <p>Enter your pseudocode and click "Generate Flowchart" to see the result</p>
            </div>
        `;
        this.downloadBtn.disabled = true;
        this.currentFlowchartData = null;
        this.hideError();
        this.autoResizeTextarea();
    }

    showLoading() {
        this.loadingIndicator.classList.remove('hidden');
        this.generateBtn.disabled = true;
        this.generateBtn.textContent = 'Generating...';
    }

    hideLoading() {
        this.loadingIndicator.classList.add('hidden');
        this.generateBtn.disabled = false;
        this.generateBtn.textContent = 'Generate Flowchart';
    }

    showError(message) {
        this.errorText.textContent = message;
        this.errorMessage.classList.remove('hidden');
        this.flowchartOutput.style.display = 'none';
    }

    hideError() {
        this.errorMessage.classList.add('hidden');
        this.flowchartOutput.style.display = 'flex';
    }

    // Utility method to validate pseudocode syntax
    validatePseudocode(code) {
        const lines = code.split('\n').map(line => line.trim()).filter(line => line);
        const errors = [];
        
        let ifCount = 0;
        let whileCount = 0;
        let forCount = 0;
        
        lines.forEach((line, index) => {
            if (line.startsWith('IF ') && line.endsWith(' THEN')) {
                ifCount++;
            } else if (line === 'ENDIF') {
                ifCount--;
                if (ifCount < 0) {
                    errors.push(`Line ${index + 1}: ENDIF without matching IF`);
                }
            } else if (line.startsWith('WHILE ') && line.endsWith(' DO')) {
                whileCount++;
            } else if (line === 'ENDWHILE') {
                whileCount--;
                if (whileCount < 0) {
                    errors.push(`Line ${index + 1}: ENDWHILE without matching WHILE`);
                }
            } else if (line.startsWith('FOR ') && line.includes(' TO ')) {
                forCount++;
            } else if (line.startsWith('NEXT ')) {
                forCount--;
                if (forCount < 0) {
                    errors.push(`Line ${index + 1}: NEXT without matching FOR`);
                }
            }
        });
        
        if (ifCount > 0) {
            errors.push('Missing ENDIF statement(s)');
        }
        if (whileCount > 0) {
            errors.push('Missing ENDWHILE statement(s)');
        }
        if (forCount > 0) {
            errors.push('Missing NEXT statement(s)');
        }
        
        return errors;
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FlowchartConverter();
});

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to generate
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('generateBtn').click();
    }
    
    // Ctrl/Cmd + S to download (if flowchart exists)
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        if (!document.getElementById('downloadBtn').disabled) {
            document.getElementById('downloadBtn').click();
        }
    }
});