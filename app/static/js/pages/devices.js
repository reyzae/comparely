// ==========================================
// DEVICES PAGE - Compare Bar Functionality
// File: devices.js
// Deskripsi: JavaScript untuk halaman devices list
// ==========================================

// Tunggu sampai halaman selesai load
document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // INISIALISASI ELEMEN
    // ==========================================

    // Ambil elemen-elemen yang diperlukan
    const compareBar = document.getElementById('compareBar');
    const selectedDevicesContainer = document.getElementById('selectedDevices');
    const compareButton = document.getElementById('compareButton');
    const clearButton = document.getElementById('clearButton');

    // View toggle elements
    const gridViewBtn = document.getElementById('gridViewBtn');
    const listViewBtn = document.getElementById('listViewBtn');
    const devicesGrid = document.getElementById('devicesGrid');
    const devicesList = document.getElementById('devicesList');

    // ==========================================
    // VARIABEL GLOBAL
    // ==========================================

    // Array untuk menyimpan device yang dipilih (maksimal 2)
    let selectedDevices = [];

    // ==========================================
    // VIEW TOGGLE FUNCTIONALITY
    // ==========================================

    // Load saved view preference from localStorage
    const savedView = localStorage.getItem('devices_view_preference') || 'grid';
    setView(savedView);

    // Event listener untuk grid view button
    if (gridViewBtn) {
        gridViewBtn.addEventListener('click', function () {
            setView('grid');
            localStorage.setItem('devices_view_preference', 'grid');
        });
    }

    // Event listener untuk list view button
    if (listViewBtn) {
        listViewBtn.addEventListener('click', function () {
            setView('list');
            localStorage.setItem('devices_view_preference', 'list');
        });
    }

    /**
     * Function untuk set view (grid atau list)
     */
    function setView(view) {
        if (view === 'grid') {
            // Show grid, hide list
            if (devicesGrid) devicesGrid.style.display = 'grid';
            if (devicesList) devicesList.style.display = 'none';

            // Update button states
            if (gridViewBtn) gridViewBtn.classList.add('active');
            if (listViewBtn) listViewBtn.classList.remove('active');
        } else {
            // Show list, hide grid
            if (devicesGrid) devicesGrid.style.display = 'none';
            if (devicesList) devicesList.style.display = 'flex';

            // Update button states
            if (gridViewBtn) gridViewBtn.classList.remove('active');
            if (listViewBtn) listViewBtn.classList.add('active');
        }
    }

    // ==========================================
    // PRICE SLIDER FUNCTIONALITY
    // ==========================================

    const priceSlider = document.getElementById('priceSlider');
    const priceValue = document.getElementById('priceValue');

    if (priceSlider && priceValue) {
        // Format number to Rupiah
        function formatRupiah(number) {
            return 'Rp ' + number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        }

        // Update price display and gradient
        function updatePriceDisplay() {
            const value = parseInt(priceSlider.value);
            priceValue.textContent = formatRupiah(value);

            // Update gradient fill
            const percentage = (value / priceSlider.max) * 100;
            priceSlider.style.background = `linear-gradient(to right, #06B6D4 0%, #06B6D4 ${percentage}%, #E5E7EB ${percentage}%, #E5E7EB 100%)`;
        }

        // Event listener for slider input
        priceSlider.addEventListener('input', updatePriceDisplay);

        // Initialize on page load
        updatePriceDisplay();
    }

    // ==========================================
    // EVENT LISTENERS
    // ==========================================

    // Event listener untuk semua checkbox device (both grid and list)
    document.querySelectorAll('.device-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const deviceId = this.getAttribute('data-id');
            const deviceName = this.getAttribute('data-name');
            const card = this.closest('.device-item-card, .device-item-list');

            if (this.checked) {
                // Tambah device ke selection
                addDevice(deviceId, deviceName, card);
            } else {
                // Remove device dari selection
                removeDevice(deviceId, card);
            }

            // Update compare bar
            updateCompareBar();

            // Sync checkboxes between grid and list view
            syncCheckboxes(deviceId, this.checked);
        });
    });

    // Event listener untuk tombol compare
    if (compareButton) {
        compareButton.addEventListener('click', function () {
            if (selectedDevices.length === 2) {
                // Redirect ke halaman compare
                window.location.href = `/compare-page?id1=${selectedDevices[0].id}&id2=${selectedDevices[1].id}`;
            }
        });
    }

    // Event listener untuk tombol clear
    if (clearButton) {
        clearButton.addEventListener('click', function () {
            // Clear semua selection
            clearSelection();
        });
    }

    // ==========================================
    // AUTO-SUBMIT SAAT KATEGORI BERUBAH
    // ==========================================

    // Ambil elemen kategori dropdown
    const categorySelect = document.getElementById('category');

    // Kalau ada kategori dropdown
    if (categorySelect) {
        // Event listener saat kategori berubah
        categorySelect.addEventListener('change', function () {
            // Ambil form
            const form = this.closest('form');

            // Submit form otomatis
            if (form) {
                form.submit();
            }
        });
    }

    // ==========================================
    // FUNCTIONS
    // ==========================================

    /**
     * Function untuk sync checkboxes antara grid dan list view
     */
    function syncCheckboxes(deviceId, checked) {
        document.querySelectorAll(`.device-checkbox[data-id="${deviceId}"]`).forEach(cb => {
            cb.checked = checked;
        });
    }

    /**
     * Function untuk tambah device ke selection
     */
    function addDevice(id, name, card) {
        // Cek apakah sudah ada 2 device
        if (selectedDevices.length >= 2) {
            // Uncheck checkbox yang baru diklik
            const checkboxes = document.querySelectorAll(`.device-checkbox[data-id="${id}"]`);
            checkboxes.forEach(cb => cb.checked = false);

            // Tampilkan pesan ke user
            alert('Maksimal 2 device untuk dibandingkan!');
            return;
        }

        // Tambah device ke array
        selectedDevices.push({ id, name });

        // Tambah class 'selected' ke semua card dengan ID yang sama
        document.querySelectorAll(`.device-checkbox[data-id="${id}"]`).forEach(cb => {
            const parentCard = cb.closest('.device-item-card, .device-item-list');
            if (parentCard) {
                parentCard.classList.add('selected');
            }
        });

        console.log('Device ditambahkan:', name);
    }

    /**
     * Function untuk remove device dari selection
     */
    function removeDevice(id, card) {
        // Filter out device yang di-remove
        selectedDevices = selectedDevices.filter(device => device.id !== id);

        // Remove class 'selected' dari semua card dengan ID yang sama
        document.querySelectorAll(`.device-checkbox[data-id="${id}"]`).forEach(cb => {
            const parentCard = cb.closest('.device-item-card, .device-item-list');
            if (parentCard) {
                parentCard.classList.remove('selected');
            }
        });

        console.log('Device dihapus, sisa:', selectedDevices.length);
    }

    /**
     * Function untuk update tampilan compare bar
     */
    function updateCompareBar() {
        // Kalau ada device yang dipilih, show compare bar
        if (selectedDevices.length > 0) {
            compareBar.classList.add('active');

            // Update list device yang dipilih
            selectedDevicesContainer.innerHTML = selectedDevices.map(device => `
                <span class="selected-device-tag">✓ ${device.name}</span>
            `).join('');

            // Enable/disable tombol compare
            if (selectedDevices.length === 2) {
                compareButton.disabled = false;
            } else {
                compareButton.disabled = true;
            }
        } else {
            // Hide compare bar kalau tidak ada device yang dipilih
            compareBar.classList.remove('active');
        }
    }

    /**
     * Function untuk clear semua selection
     */
    function clearSelection() {
        // Uncheck semua checkbox
        document.querySelectorAll('.device-checkbox').forEach(checkbox => {
            checkbox.checked = false;

            // Remove selected class dari card
            const card = checkbox.closest('.device-item-card, .device-item-list');
            if (card) {
                card.classList.remove('selected');
            }
        });

        // Clear array
        selectedDevices = [];

        // Update compare bar
        updateCompareBar();

        console.log('Selection cleared');
    }

    // ==========================================
    // FADE-IN ANIMATION
    // ==========================================

    // Add fade-in animation ke device cards saat page load
    addFadeInAnimation('.device-item-card');
    addFadeInAnimation('.device-item-list');

});
