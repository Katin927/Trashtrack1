document.addEventListener('DOMContentLoaded', () => {

  // ✅ Tip Carousel
  const slides = document.querySelectorAll('#tips-carousel .tip-slide');
  let currentSlide = 0;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
    });
  }

  if (slides.length > 0) {
    showSlide(currentSlide);

    setInterval(() => {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    }, 3000);
  }

  // ✅ Chart
  const chartDataEl = document.getElementById('chart-data');
  const chartData = JSON.parse(chartDataEl.textContent);
  let chart;

  function drawChart(data) {
    const ctx = document.getElementById('waste-chart').getContext('2d');
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'pie',
      data: {
        labels: Object.keys(data),
        datasets: [{
          data: Object.values(data),
          backgroundColor: ['#7FB3D5', '#F7DC6F', '#F1948A', '#82E0AA', '#BB8FCE']
        }]
      },
      options: {
        responsive: false,
        plugins: { legend: { position: 'bottom' } }
      }
    });
  }
  drawChart(chartData.all);

  document.getElementById('chart-toggle').addEventListener('change', (e) => {
    drawChart(e.target.value === 'recent' ? chartData.recent : chartData.all);
  });

  // ✅ Barcode Lookup
  document.getElementById('barcode-lookup').addEventListener('click', async () => {
    const code = document.getElementById('dashboard-barcode').value.trim();
    if (!code) return;

    const res = await fetch('/waste/api/lookup-barcode', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ barcode: code })
    });

    const data = await res.json();
    if (data.item_name) document.getElementById('dashboard-item').value = data.item_name;
    if (data.category) document.getElementById('dashboard-category').value = data.category;
    if (data.disposal_method) document.getElementById('dashboard-disposal').value = data.disposal_method; // ✅ NEW: fill disposal method
  });

  // ✅ Log Waste
  document.getElementById('dashboard-log').addEventListener('click', async () => {
    const item = document.getElementById('dashboard-item').value.trim();
    const category = document.getElementById('dashboard-category').value;
    if (!item || !category) {
      alert('Please fill out both fields.');
      return;
    }

    const res = await fetch('/waste/api/log-waste', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ item_name: item, category })
    });

    if (res.ok) {
      showToast('🎉 Congrats! Waste successfully logged!');
      setTimeout(() => location.reload(), 2000);
    } else {
      alert('Failed to log waste.');
    }
  });

  // ✅ Toast Notification
  function showToast(message) {
    const toastEl = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    toastMessage.textContent = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
  }

  // ✅ Delete Waste
  document.querySelectorAll('.delete-btn').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const id = btn.dataset.id;
      const res = await fetch(`/waste/api/log-waste/${id}`, { method: 'DELETE' });
      if (res.ok) {
        btn.closest('li').remove();
      } else {
        alert('Failed to delete waste log.');
      }
    });
  });

  // ✅ Light/Dark Mode Toggle
  const modeToggleBtn = document.getElementById('mode-toggle');
  const dashboardContainer = document.querySelector('.dashboard-container');

  modeToggleBtn.addEventListener('click', () => {
    dashboardContainer.classList.toggle('light-mode');
    dashboardContainer.classList.toggle('dark-mode');
  });

});
