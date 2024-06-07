import sys
import time

def perencanaan_persediaan_branch_and_bound(permintaan, kapasitas, biaya_penyimpanan, biaya_pemesanan, biaya_kekurangan):
    """
    Algoritma Branch and Bound untuk perencanaan persediaan.

    Args:
        permintaan: Daftar permintaan terprediksi untuk setiap periode.
        kapasitas: Kapasitas maksimum gudang.
        biaya_penyimpanan: Biaya penyimpanan per unit per periode.
        biaya_pemesanan: Biaya pemesanan per pesanan.
        biaya_kekurangan: Biaya kekurangan persediaan per unit.

    Returns:
        Daftar tingkat persediaan optimal untuk setiap periode, total biaya kumulatif, total biaya persediaan, dan waktu eksekusi.
    """
    
    n = len(permintaan)  # Jumlah periode
    inventori_terbaik = [0] * n  # Daftar inventori terbaik di setiap periode

    # Inisialisasi biaya total minimum
    biaya_total_minimum = sys.maxsize  # Gunakan nilai maksimum sebagai awal

    def hitung_biaya(inventori, permintaan):
        """Menghitung biaya total berdasarkan tingkat inventori dan permintaan."""
        total_biaya = 0
        inventori_saat_ini = 0
        
        for i in range(len(permintaan)):
            # Tambahkan inventori baru
            inventori_saat_ini += inventori[i]
            
            if inventori_saat_ini < permintaan[i]:  # Kekurangan persediaan
                total_biaya += biaya_kekurangan * (permintaan[i] - inventori_saat_ini)
                inventori_saat_ini = 0
            else:
                inventori_saat_ini -= permintaan[i]
                total_biaya += biaya_penyimpanan * inventori_saat_ini

        return total_biaya

    start_time = time.time()

    def branch_and_bound(periode, inventori_saat_ini, biaya_saat_ini, rencana_inventori):
        """Algoritma Branch and Bound untuk menemukan solusi optimal."""
        nonlocal biaya_total_minimum, inventori_terbaik

        if periode == n:
            if biaya_saat_ini < biaya_total_minimum:
                biaya_total_minimum = biaya_saat_ini
                inventori_terbaik = rencana_inventori[:]
            return

        # Pertimbangkan semua level inventori yang mungkin untuk periode ini
        for tingkat_inventori in range(kapasitas + 1):
            rencana_inventori_berikutnya = rencana_inventori[:]
            rencana_inventori_berikutnya[periode] = tingkat_inventori

            biaya_berikutnya = hitung_biaya(rencana_inventori_berikutnya, permintaan[:periode + 1]) + (biaya_pemesanan if tingkat_inventori > 0 else 0)
            if biaya_berikutnya < biaya_total_minimum:
                branch_and_bound(periode + 1, inventori_saat_ini + tingkat_inventori - permintaan[periode], biaya_berikutnya, rencana_inventori_berikutnya)

    branch_and_bound(0, 0, 0, [0] * n)

    end_time = time.time()
    execution_time = end_time - start_time
    
    total_biaya_persediaan = sum(inventori_terbaik) * biaya_penyimpanan
    return inventori_terbaik, biaya_total_minimum, total_biaya_persediaan, round(execution_time, 2)

permintaan = [70, 320, 320, 40, 30, 50]
kapasitas = 300
biaya_penyimpanan = 10
biaya_pemesanan = 50
biaya_kekurangan = 20

inventori_optimal, total_biaya, total_biaya_persediaan, execution_time = perencanaan_persediaan_branch_and_bound(permintaan, kapasitas, biaya_penyimpanan, biaya_pemesanan, biaya_kekurangan)

print(f"Tingkat Persediaan Optimal: {inventori_optimal}")
print(f"Total Biaya: {total_biaya}")
print(f"Total Biaya Persediaan: {total_biaya_persediaan}")
print(f"Execution Time: {execution_time:.10f}s")