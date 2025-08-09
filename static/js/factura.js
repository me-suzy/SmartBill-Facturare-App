document.addEventListener('DOMContentLoaded', function() {
    const facturaForm = document.getElementById('facturaForm');
    const addProductBtn = document.getElementById('addProduct');
    const productsTable = document.getElementById('productsTable');

    // Adaugă produs
    addProductBtn.addEventListener('click', function() {
        addProductRow();
    });

    // Salvează factura
    facturaForm.addEventListener('submit', function(e) {
        e.preventDefault();
        saveFactura();
    });

    function addProductRow() {
        const tbody = productsTable.querySelector('tbody');
        const rowCount = tbody.children.length;

        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${rowCount}</td>
            <td><input type="text" name="denumire" placeholder="Denumire produs/serviciu" required></td>
            <td>
                <select name="um">
                    <option value="buc">buc</option>
                    <option value="kg">kg</option>
                    <option value="ore">ore</option>
                    <option value="mp">mp</option>
                </select>
            </td>
            <td><input type="number" name="cantitate" min="1" value="1" required></td>
            <td><input type="number" name="pret" step="0.01" min="0" required></td>
            <td class="valoare">0.00</td>
        `;

        // Înlocuiește rândul de adăugare
        const addRow = document.getElementById('addProductRow');
        tbody.insertBefore(newRow, addRow);

        // Adaugă event listeners pentru calcul
        const cantitateInput = newRow.querySelector('input[name="cantitate"]');
        const pretInput = newRow.querySelector('input[name="pret"]');
        const valoareCell = newRow.querySelector('.valoare');

        function calculateValue() {
            const cantitate = parseFloat(cantitateInput.value) || 0;
            const pret = parseFloat(pretInput.value) || 0;
            const valoare = cantitate * pret;
            valoareCell.textContent = valoare.toFixed(2);
        }

        cantitateInput.addEventListener('input', calculateValue);
        pretInput.addEventListener('input', calculateValue);
    }

    function saveFactura() {
        const formData = new FormData(facturaForm);
        const facturaData = {
            client_cif: formData.get('clientCIF'),
            data_emitere: formData.get('dataEmitere'),
            moneda: formData.get('moneda'),
            limba: formData.get('limba'),
            produse: []
        };

        // Colectează produsele
        const rows = productsTable.querySelectorAll('tbody tr:not(#addProductRow)');
        rows.forEach(row => {
            const inputs = row.querySelectorAll('input, select');
            if (inputs.length > 0) {
                const produs = {
                    denumire: row.querySelector('input[name="denumire"]').value,
                    um: row.querySelector('select[name="um"]').value,
                    cantitate: row.querySelector('input[name="cantitate"]').value,
                    pret: row.querySelector('input[name="pret"]').value
                };
                facturaData.produse.push(produs);
            }
        });

        // Trimite la server
        fetch('/api/save_factura', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(facturaData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Factura a fost salvată cu succes!');
                window.location.href = '/dashboard';
            } else {
                alert('Eroare la salvarea facturii!');
            }
        })
        .catch(error => {
            console.error('Eroare:', error);
            alert('Eroare la salvarea facturii!');
        });
    }
});