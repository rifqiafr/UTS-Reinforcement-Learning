# 🎮 Reinforcement-Learning KELOMPOK 3
1. RIMAYA DWI ATIKA (G1A021021)
2. MUHAMAD RIFQI AFRIANSYAH (G1A021023)
3. ILHAM DIO PUTRA (G1A021024)

## 🚀 GAME GRID WORLD

Grid World adalah sebuah lingkungan simulasi yang digunakan dalam pembelajaran penguatan (reinforcement learning) untuk mengajarkan agen bagaimana membuat keputusan berdasarkan interaksi dengan lingkungan. 
Dalam game ini, agen bergerak di atas grid persegi yang terdiri dari beberapa sel, di mana setiap sel dapat memiliki status yang berbeda, seperti sel kosong, sel tujuan, atau sel berbahaya. 
Agen dapat melakukan tindakan dengan bergerak ke atas, bawah, kiri, atau kanan, dan menerima hadiah (reward) berdasarkan posisi yang dicapainya. 
Tujuan utama agen adalah mencapai sel tujuan dengan mengumpulkan poin sebanyak mungkin, sambil belajar dari pengalaman sebelumnya untuk menghindari sel berbahaya dan memilih langkah yang paling optimal.

### 🎥 Visualisasi
Game ini memperlihatkan grid berukuran 5x5, di mana:
- **Warna Merah**: Agen
- **Warna Hijau**: Posisi Awal
- **Warna Biru**: Tujuan
- **Warna Abu-abu**: Penghalang
- **Warna Putih**: Ruang Kosong

## 🕹️ PENERAPAN ALGORITMA MARKOV DECISION PROCESS

![Video Game Cover](link_to_image)
![image](https://github.com/user-attachments/assets/c135001f-0224-4c50-8979-a317c385bfbc)
Hasil output menampilkan dua bagian utama: jendela game dan terminal.
Di jendela game, terdapat grid 5x5 yang berfungsi sebagai area permainan. Setiap cell memiliki warna berbeda: putih untuk ruang kosong, abu-abu untuk dinding, hijau untuk cell reward, dan biru untuk tujuan akhir. Posisi awal pemain ditandai dengan lingkaran merah, dan pemain bergerak secara otomatis mengikuti aksi yang dipilih oleh AI.
Di terminal, tercetak log pergerakan pemain, seperti "Player moves up to position [3, 2]", yang menunjukkan koordinat tujuan. AI menggunakan pendekatan Markov Decision Process (MDP) untuk memilih aksi terbaik dan meminimalkan jarak pemain ke tujuan menggunakan jarak Manhattan. Setelah mencapai tujuan di (0, 4), terminal menampilkan pesan "Goal reached!", menandakan bahwa permainan telah selesai.

## 🎯 PENERAPAN ALGORITMA POLICY BELLMAN EQUATION
![Video Game Cover](link_to_image)
![WhatsApp Image 2024-10-16 at 16 26 29_58158e6a](https://github.com/user-attachments/assets/975d700e-bc50-4155-9c4e-6e55d70faa86)
Hasil output terdiri dari dua bagian utama: visualisasi grafis permainan "Robot Grid World" menggunakan Pygame dan representasi tekstual posisi robot di terminal.
Pada visualisasi, tampak grid labirin berukuran 5x5 dengan sel berwarna yang menunjukkan elemen-elemen di dalamnya: sel putih sebagai ruang bebas, sel abu-abu sebagai dinding, lingkaran merah sebagai posisi robot, dan sel biru sebagai tujuan di sudut kanan atas. Robot bergerak mengikuti kebijakan optimal dari algoritma Policy Iteration.
Di bagian terminal, grid ditampilkan dalam format teks yang menunjukkan posisi robot (R), dinding (#), tujuan (G), dan ruang kosong (.). Setiap langkah memperlihatkan pergerakan robot menuju tujuan, dan ketika robot mencapai sel tujuan, terminal mencetak pesan "Goal reached!", menandakan bahwa simulasi telah berhasil.

## 💡 PENERAPAN ALGORITMA Q-FUNCTION VALUE ITERATION
![Video Game Cover](link_to_image)
![image](https://github.com/user-attachments/assets/ea77db5a-a579-4594-9e69-7684c43e8ce8)
Output di atas menampilkan permainan Grid World yang menerapkan konsep Q-function dan Value Iteration. Agen ditandai dengan warna merah, posisi awal dengan warna hijau, dan tujuan dengan warna biru. Sel abu-abu mewakili penghalang dan penalti, sedangkan sel putih adalah ruang kosong yang dapat dilalui.
Grafik menunjukkan agen yang berhasil mencapai tujuan, ditandai dengan catatan "Goal reached!" yang mencerminkan efektivitas algoritma. Sementara itu, output terminal mencetak status grid di setiap langkah, di mana nilai Q diperbarui berdasarkan tindakan yang diambil. Q-function mengevaluasi nilai tindakan untuk memaksimalkan reward, sedangkan Value Iteration menghitung nilai optimal melalui iterasi berulang, memungkinkan agen merencanakan jalur terbaik.

## ⭐ KESIMPULAN
Berdasarkan penerapan tiga algoritma pada game Grid World—Markov Decision Process (MDP), Policy Iteration dengan Bellman Equation, dan Q-function Value Iteration—dapat disimpulkan bahwa masing-masing memiliki keunggulan dan kelemahan.
MDP efektif dalam situasi ketidakpastian dengan transisi stokastik, tetapi lebih lambat karena banyaknya probabilitas yang harus dihitung. Policy Iteration dengan Bellman Equation menawarkan stabilitas dan efisiensi yang lebih baik, fokus pada perbaikan kebijakan tanpa memperhitungkan probabilitas stokastik. Sementara itu, Q-function Value Iteration menggabungkan Value Iteration dan Q-learning, memungkinkan pembaruan nilai Q berdasarkan reward dan nilai state berikutnya, dengan konvergensi lebih cepat.
Oleh karena itu, Q-function Value Iteration direkomendasikan sebagai algoritma paling efektif untuk game Grid World.

## 📖 CARA RUN GAME
```bash
# Clone repository
git clone https://github.com/[username]/[repository].git

# Buka folder pada Visual Studio Code, di terminal
pip install pygame

# Jalankan game
python namafile.py

# 📚 Referensi
- https://github.com/brianspiering/rl-course/tree/cca8cc7ded9f40ba3860a53282a5f44a01f38d1a/02_policy__value_iteration

