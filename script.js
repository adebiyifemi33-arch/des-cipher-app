document.addEventListener('DOMContentLoaded', () => {
    const keyInput = document.getElementById('key');
    const keyCounter = document.getElementById('key-counter');
    const textInput = document.getElementById('text');
    const outputText = document.getElementById('output');
    const btnEncrypt = document.getElementById('btn-encrypt');
    const btnDecrypt = document.getElementById('btn-decrypt');
    const btnCopy = document.getElementById('btn-copy');
    const errorMsg = document.getElementById('error-message');

    // Update key length counter
    keyInput.addEventListener('input', () => {
        const len = keyInput.value.length;
        keyCounter.textContent = `${len}/8`;
        if (len === 8) {
            keyCounter.style.color = 'var(--neon-cyan)';
        } else {
            keyCounter.style.color = '#888';
        }
    });

    const showError = (message) => {
        errorMsg.textContent = message;
        errorMsg.classList.remove('hidden');
        setTimeout(() => {
            errorMsg.classList.add('hidden');
        }, 5000);
    };

    const processData = async (action) => {
        const key = keyInput.value;
        const text = textInput.value;

        if (key.length !== 8) {
            showError('ERROR: Key must be exactly 8 characters long.');
            return;
        }

        if (!text) {
            showError('ERROR: Payload data cannot be empty.');
            return;
        }

        try {
            const response = await fetch(`/api/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ key, text })
            });

            const data = await response.json();

            if (!response.ok) {
                showError(`SYSTEM ERROR: ${data.detail || 'Unknown error'}`);
            } else {
                outputText.value = data.result;
            }
        } catch (err) {
            showError('NETWORK ERROR: Cannot reach the server.');
        }
    };

    btnEncrypt.addEventListener('click', () => processData('encrypt'));
    btnDecrypt.addEventListener('click', () => processData('decrypt'));

    btnCopy.addEventListener('click', () => {
        if (!outputText.value) return;
        outputText.select();
        document.execCommand('copy');
        
        const originalText = btnCopy.querySelector('.btn-text').textContent;
        btnCopy.querySelector('.btn-text').textContent = 'COPIED!';
        setTimeout(() => {
            btnCopy.querySelector('.btn-text').textContent = originalText;
        }, 2000);
    });
});
