let currentIndex = 0;

function showSchedule(index) {
  const blocks = document.querySelectorAll('.schedule-block');
  if (blocks.length === 0) return;

  blocks.forEach(b => b.classList.remove('active'));

  if (index < 0) index = blocks.length - 1;
  if (index >= blocks.length) index = 0;

  blocks[index].classList.add('active');
  currentIndex = index;
}

function nextSchedule() {
  showSchedule(currentIndex + 1);
}

function prevSchedule() {
  showSchedule(currentIndex - 1);
}

function setupFuzzyFinder() {
  const input = document.getElementById('searchBox');
  input.addEventListener('keyup', () => {
    const filter = input.value.toLowerCase();
    const activeBlock = document.querySelector('.schedule-block.active');
    if (!activeBlock) return;

    const rows = activeBlock.querySelectorAll('tbody tr');
    rows.forEach(row => {
      row.classList.remove('highlight');
      const text = row.textContent.toLowerCase();
      if (filter && text.includes(filter)) {
        row.classList.add('highlight');
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  showSchedule(0);  // show first schedule by default
  setupFuzzyFinder();
});

