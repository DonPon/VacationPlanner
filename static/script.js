function updateBlocks() {
    const rows = document.querySelectorAll('#vacation_table tbody tr');
    let blocks_franz = [];
    let blocks_polina = [];

    rows.forEach(row => {
        const name_input = row.querySelector('.name');
        const name = name_input ? name_input.value : row.cells[0].innerText;
        const start = row.querySelector('.start_date').value;
        const end_franz = row.querySelector('.end_franz').value;
        const end_polina = row.querySelector('.end_polina').value;

        blocks_franz.push({name, start, end_date_str: end_franz});
        blocks_polina.push({name, start, end_date_str: end_polina});
    });

    const total_franz = parseInt(document.getElementById('total_franz').value) || 0;
    const total_polina = parseInt(document.getElementById('total_polina').value) || 0;

    fetch('/update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            vacation_days_allowed_franz: total_franz,
            vacation_days_allowed_polina: total_polina,
            blocks_franz: blocks_franz,
            blocks_polina: blocks_polina
        })
    })
    .then(res => res.json())
    .then(data => {
        data.blocks_franz.forEach((block, i) => {
            const row = rows[i];
            row.querySelector('.used_franz').innerText = block.used;
            row.querySelector('.total_off_franz').innerText = block.total_days_off;
        });
        data.blocks_polina.forEach((block, i) => {
            const row = rows[i];
            row.querySelector('.used_polina').innerText = block.used;
            row.querySelector('.total_off_polina').innerText = block.total_days_off;
        });

        document.getElementById('remaining_franz').innerText = data.remaining_franz;
        document.getElementById('remaining_polina').innerText = data.remaining_polina;
    });
}

document.getElementById('add_block_btn').addEventListener('click', () => {
    const table_body = document.querySelector('#vacation_table tbody');
    const new_row = document.createElement('tr');
    new_row.innerHTML = `
        <td><input type="text" class="name" placeholder="Vacation Name"></td>
        <td><input type="date" class="start_date"></td>
        <td class="franz-col"><input type="date" class="end_franz"></td>
        <td class="polina-col"><input type="date" class="end_polina"></td>
        <td class="used_franz franz-col">0</td>
        <td class="used_polina polina-col">0</td>
        <td class="total_off_franz franz-col">0</td>
        <td class="total_off_polina polina-col">0</td>
        <td><button class="delete_btn">Delete</button></td>
    `;
    table_body.appendChild(new_row);

    new_row.querySelectorAll('.start_date, .end_franz, .end_polina, .name').forEach(input => {
        input.addEventListener('input', updateBlocks);
    });

    new_row.querySelector('.delete_btn').addEventListener('click', () => {
        new_row.remove();
        updateBlocks();
    });
});

document.querySelectorAll('.start_date, .end_franz, .end_polina').forEach(input => {
    input.addEventListener('input', updateBlocks);
});
document.getElementById('total_franz').addEventListener('input', updateBlocks);
document.getElementById('total_polina').addEventListener('input', updateBlocks);
