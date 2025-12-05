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

    // ==========================================
    // VARIABEL GLOBAL
    // ==========================================

    // Array untuk menyimpan device yang dipilih (maksimal 2)
    let selectedDevices = [];

    // ==========================================
    // EVENT LISTENERS
    // ==========================================

    // Event listener untuk semua checkbox device
    document.querySelectorAll('.device-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const deviceId = this.getAttribute('data-id');
            const deviceName = this.getAttribute('data-name');
            const card = this.closest('.device-item-card');

            if (this.checked) {
                // Tambah device ke selection
                addDevice(deviceId, deviceName, card);
            } else {
                // Remove device dari selection
                removeDevice(deviceId, card);
            }

            // Update compare bar
            updateCompareBar();
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
     * Function untuk tambah device ke selection
     */
    function addDevice(id, name, card) {
        // Cek apakah sudah ada 2 device
        if (selectedDevices.length >= 2) {
            // Uncheck checkbox yang baru diklik
            const checkbox = card.querySelector('.device-checkbox');
            checkbox.checked = false;

            // Tampilkan pesan ke user
            alert('Maksimal 2 device untuk dibandingkan!');
            return;
        }

        // Tambah device ke array
        selectedDevices.push({ id, name });

        // Tambah class 'selected' ke card
        card.classList.add('selected');

        console.log('Device ditambahkan:', name);
    }

    /**
     * Function untuk remove device dari selection
     */
    function removeDevice(id, card) {
        // Filter out device yang di-remove
        selectedDevices = selectedDevices.filter(device => device.id !== id);

        // Remove class 'selected' dari card
        card.classList.remove('selected');

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
            const card = checkbox.closest('.device-item-card');
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

});
