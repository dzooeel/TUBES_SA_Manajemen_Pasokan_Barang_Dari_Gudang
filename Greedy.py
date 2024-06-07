import time

def perencanaan_persediaan_greedy(permintaan, kapasitas, biaya_penyimpanan, biaya_pemesanan, biaya_kekurangan):
    """
    Algoritma Greedy untuk perencanaan persediaan.

    Args:
        permintaan: Daftar permintaan terprediksi untuk setiap periode.
        kapasitas: Kapasitas maksimum gudang.
        biaya_penyimpanan: Biaya penyimpanan per unit per periode.
        biaya_pemesanan: Biaya pemesanan per pesanan.
        biaya_kekurangan: Biaya kekurangan persediaan per unit.

    Returns:
        Daftar tingkat persediaan optimal untuk setiap periode, total biaya kumulatif, dan total biaya persediaan.
    """
    start_time = time.time()  # Waktu awal proses

    n = len(permintaan)  # Jumlah periode
    inventori = [0] * n  # Daftar inventori di setiap periode
    total_biaya = 0
    inventori_saat_ini = 0

    for i in range(n):
        if inventori_saat_ini < permintaan[i]:
            pesanan = min(kapasitas, permintaan[i] - inventori_saat_ini)
            inventori[i] = pesanan
            total_biaya += biaya_pemesanan
            inventori_saat_ini += pesanan
        
        inventori_saat_ini -= permintaan[i]
        
        if inventori_saat_ini < 0:
            total_biaya += abs(inventori_saat_ini) * biaya_kekurangan
            inventori_saat_ini = 0
        else:
            total_biaya += inventori_saat_ini * biaya_penyimpanan

    total_biaya_persediaan = sum(inventori) * biaya_penyimpanan

    end_time = time.time()  # Waktu akhir proses
    processing_time = end_time - start_time  # Waktu total proses
    return inventori, total_biaya, total_biaya_persediaan, processing_time

# Contoh penggunaan:
permintaan = [70, 320, 320, 40, 30, 50]
kapasitas = 300
biaya_penyimpanan = 10
biaya_pemesanan = 50
biaya_kekurangan = 20

inventori_optimal, total_biaya, total_biaya_persediaan, processing_time = perencanaan_persediaan_greedy(permintaan, kapasitas, biaya_penyimpanan, biaya_pemesanan, biaya_kekurangan)

print(f"Tingkat Persediaan Optimal: {inventori_optimal}")
print(f"Total Biaya: {total_biaya}")
print(f"Total Biaya Persediaan: {total_biaya_persediaan}")
print(f"Waktu Proses: {processing_time:.10f}s")