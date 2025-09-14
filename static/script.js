function updateBlocks() {
    const rows = document.querySelectorAll('#vacation_table tbody tr');
    let blocks_franz = [];
    let blocks_polina = [];

    rows.forEach(row => {
        const start = row.querySelector('.start_date').value;
        const used_franz = parseInt(row.querySelector('.used_franz').value) || 0;
        const used_polina = parseInt(row.querySelector('.used_polina').value) || 0;
        const name = row.cells[0].innerText;
        blocks_franz.push({name, start, used: used_franz});
        blocks_polina.push({name, start, used: used_polina});
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
            row.querySelector('.end_franz').innerText = block.end;
            row.querySelector('.total_off_franz').innerText = block.total_days_off;
        });
        data.blocks_polina.forEach((block, i) => {
            const row = rows[i];
            row.querySelector('.end_polina').innerText = block.end;
            row.querySelector('.total_off_polina').innerText = block.total_days_off;
        });

        document.getElementById('remaining_franz').innerText = data.remaining_franz;
        document.getElementById('remaining_polina').innerText = data.remaining_polina;
    });
}

document.querySelectorAll('.used_franz, .used_polina, .start_date').forEach(input => {
    input.addEventListener('input', updateBlocks);
});
document.getElementById('total_franz').addEventListener('input', updateBlocks);
document.getElementById('total_polina').addEventListener('input', updateBlocks);
