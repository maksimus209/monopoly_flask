// Funkcja do rzucania kostką
function rollDice() {
    fetch('/roll-dice')
        .then(response => response.json())
        .then(data => {
            // Wyświetl wynik rzutu
            document.getElementById('dice-result').textContent =
                `Gracz ${data.player} rzucił kostką: ${data.dice_roll}. Nowa pozycja: ${data.new_position}`;

            // Odśwież stronę, aby zaktualizować planszę i pozycje graczy
            location.reload();
        })
        .catch(error => console.error('Błąd:', error));
}
