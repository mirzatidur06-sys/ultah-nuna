import os
from flask import Flask, render_template_string, send_from_directory

app = Flask(__name__)

@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Birthday Gift For You</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Caveat:wght@700&display=swap" rel="stylesheet">
    <style>
        body {
            margin:0; font-family:'Poppins', sans-serif;
            background: linear-gradient(135deg,#ffd3e9,#cfe7ff);
            min-height:100vh; display:flex; justify-content:center; align-items:center;
            overflow-x:hidden; position:relative;
        }
        
        /* Floating Sticker */
        .emblem-wrapper {
            position:fixed; top:15px; right:15px; width:70px; height:70px; 
            animation: emblemFloat 3s ease-in-out infinite; z-index: 100;
        }
        @keyframes emblemFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(8deg); }
        }
        .emblem { width:100%; filter: drop-shadow(0 0 5px rgba(0,0,0,0.1)); }

        /* Pages System */
        .page { 
            position:absolute; width:90%; max-width:450px; text-align:center; 
            transition: all 0.6s ease; opacity:0; pointer-events:none; display: none;
        }
        .show { 
            opacity:1 !important; pointer-events:auto !important; 
            transform:translateY(0) !important; position: relative; display: block; 
        }

        .btn {
            padding:12px 25px; background:#ff82a9; color:white; border:none; 
            border-radius:50px; font-size:16px; font-weight:600; cursor:pointer; 
            transition:.3s; box-shadow: 0 4px 15px rgba(255,130,169,0.4); margin-top: 15px;
        }
        .btn:hover { transform:scale(1.05); background:#ff6c99; }
        
        .card { 
            background:#fff; border-radius:20px; padding:25px; 
            box-shadow:0 15px 35px rgba(0,0,0,0.1); margin-bottom: 20px;
        }

        /* Countdown Style */
        .timer-wrapper { margin-top: 20px; display: flex; justify-content: center; gap: 10px; }
        .time-unit { background: white; padding: 10px; border-radius: 10px; min-width: 50px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
        .time-unit span { display: block; font-weight: bold; color: #ff82a9; font-size: 20px; }
        .time-unit label { font-size: 9px; text-transform: uppercase; color: #888; }

        /* Kado Animation */
        #giftEmoji { font-size:90px; cursor:pointer; margin-bottom: 20px; animation: giftBounce 1.2s ease-in-out infinite; }
        @keyframes giftBounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-20px); } }

        /* Gallery Landscape */
        #pageGallery { display: none; width: 100%; max-width: 600px; padding: 20px; box-sizing: border-box; }
        .gallery-list { display: flex; flex-direction: column; gap: 25px; width: 100%; }
        .photo-item { 
            background: white; padding: 12px; border-radius: 10px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.08); transform: rotate(-1deg);
        }
        .photo-item:nth-child(even) { transform: rotate(1deg); }
        .photo-item img { 
            width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 5px;
        }
        .photo-item p { font-family: 'Caveat', cursive; font-size: 20px; margin: 10px 0 0 0; color: #444; }

        /* Textarea for Message */
        textarea {
            width: 100%; height: 120px; padding: 15px; border-radius: 15px;
            border: 2px solid #ffd3e9; font-family: inherit; font-size: 15px;
            box-sizing: border-box; outline: none; margin-top: 10px;
        }
    </style>
</head>
<body>

<div class="emblem-wrapper">
    <img class="emblem" src="https://cdn-icons-png.flaticon.com/512/1147/1147981.png">
</div>

<audio id="birthdaySong" src="https://files.catbox.moe/wsgxyt.mp4" loop></audio>

<div id="pageLocked" class="page show">
    <img style="width:120px;" src="https://cdn-icons-png.flaticon.com/512/3850/3850285.png">
    <h1 style="font-family:'Caveat', cursive; font-size: 35px;">Tunggu ya... ❤️</h1>
    <p>Hadiah spesial ini bakal kebuka dalam:</p>
    <div class="timer-wrapper">
        <div class="time-unit"><span id="d">00</span><label>Hari</label></div>
        <div class="time-unit"><span id="h">00</span><label>Jam</label></div>
        <div class="time-unit"><span id="m">00</span><label>Menit</label></div>
        <div class="time-unit"><span id="s">00</span><label>Detik</label></div>
    </div>
    <p style="margin-top:20px; font-size: 12px; color: #ff82a9; font-weight: bold;">7 Januari 2026, 00:00 WIB</p>
</div>

<div id="page1" class="page">
    <img style="width:120px;" src="https://cdn-icons-png.flaticon.com/512/4392/4392525.png">
    <h1>Haii! Sebelum lanjut,<br>isi dulu data diri kamu yaa 🌸</h1>
    <button class="btn" onclick="switchPage('page2')">Gaskeun! 🚀</button>
</div>

<div id="page2" class="page">
    <div class="card">
        <h1>Kenalan dulu yuk 🤭</h1>
        <input type="text" id="nama" style="width:100%; padding:12px; margin:10px 0; border-radius:10px; border:1px solid #ddd;" placeholder="Nama kamu">
        <input type="number" id="umur" style="width:100%; padding:12px; margin:10px 0; border-radius:10px; border:1px solid #ddd;" placeholder="Umur kamu?">
        <button class="btn" onclick="startSurprise()">Kirim & Lihat Kejutan ~</button>
    </div>
</div>

<div id="page3" class="page">
    <h1>Menyiapkan Kejutan...</h1>
    <div id="timer" style="font-size:60px; font-weight:bold; color:#ff82a9;">3</div>
</div>

<div id="page4" class="page">
    <div id="giftEmoji" onclick="revealCard()">🎁</div>
    <h2>Klik kadonya! ✨</h2>
</div>

<div id="page5" class="page">
    <div class="card">
        <h2 id="ucapanText"></h2>
        <button class="btn" onclick="showGallery()">Lihat Kenangan ✨</button>
    </div>
</div>

<div id="pageGallery">
    <h2 style="color:#ff6c99; font-family:'Caveat', cursive; font-size:35px; text-align:center;">Our Memories ❤️</h2>
    <div class="gallery-list">
        <div class="photo-item"><img src="https://files.catbox.moe/wfyphd.png"><p>Foto berdua kita yang menurutku paling romantis+lucu</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/na59r1.png"><p>Ni aku gendong orang terlucu di dunia</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/ezpsil.png"><p>Pas kita main konon ni yang kamu bilang berani</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/2o84c5.png"><p>Pas naik gunung ni awal awal hts</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/m4gjt7.png"><p>Makasih yahh dah mau nolongin</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/62rvez.png"><p>Semoga kita begini terus yahh</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/s04vxf.png"><p>Nanti jatuh nangis eluu</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/kuv421.png"><p>Sehat selalu ya kamu.</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/g23me7.png"><p>Satu kata: imutt!</p></div>
        <div class="photo-item"><img src="https://files.catbox.moe/slczyl.png"><p>Pertama x kita foto ni sama teman kita</p></div>
    </div>
    <div style="text-align: center; margin: 30px 0;">
        <button class="btn" onclick="showFinalMessage()">Tulis Pesan untukku ✨</button>
    </div>
</div>

<div id="pageFinal" class="page">
    <div class="card">
        <h2>Kirim Pesan 🎉</h2>
        <p>Tulis harapan atau pesanmu di sini yaa:</p>
        <textarea id="pesanWA" placeholder="Tulis sesuatu yang manis..."></textarea>
        <button class="btn" style="background: #25d366;" onclick="kirimKeWA()">Kirim ke WhatsApp 📱</button>
    </div>
</div>

<script>
// PENGATURAN WAKTU BUKA: 7 JANUARI 2026 JAM 00:00:00
const targetDate = new Date("Jan 7, 2026 00:00:00").getTime();

let userNama = "";
let userUmur = "";
const nomorWA = "6281264247474"; 

// Fungsi Timer Countdown
const x = setInterval(function() {
    const now = new Date().getTime();
    const distance = targetDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById("d").innerHTML = days;
    document.getElementById("h").innerHTML = hours;
    document.getElementById("m").innerHTML = minutes;
    document.getElementById("s").innerHTML = seconds;

    // Jika waktu sudah tercapai atau lewat
    if (distance < 0) {
        clearInterval(x);
        // Pindah otomatis ke halaman 1 jika masih di halaman lock
        if(document.getElementById('pageLocked').style.display !== 'none') {
            switchPage('page1');
        }
    }
}, 1000);

function switchPage(id){
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('show');
        p.style.display = 'none';
    });
    const target = document.getElementById(id);
    if(target) {
        target.style.display = 'block';
        setTimeout(() => target.classList.add('show'), 50);
    }
}

function startSurprise(){
    userNama = document.getElementById('nama').value || "Sayang";
    userUmur = document.getElementById('umur').value || "Spesial";
    switchPage('page3');
    let time = 3;
    const tDisplay = document.getElementById('timer');
    const countdown = setInterval(() => {
        time--;
        tDisplay.textContent = time;
        if(time <= 0){
            clearInterval(countdown);
            switchPage('page4');
        }
    }, 1000);
}

function revealCard(){
    document.getElementById('birthdaySong').play();
    const ucapan = document.getElementById('ucapanText');
    ucapan.innerHTML = `Happy Birthday, <br><span style="color:#ff82a9; font-size:35px;">${userNama}!</span> 🎉<br><br>Gak terasa sekarang udah ${userUmur} tahun aja, aku harap kamu menjadi anak yang baik,ramah,jujur kepada siapa pun, dan kita harus langgeng yahhh..
Kita harus saling percaya biar hubungan kita kuat dan kalo ada masalah kita harus cari jalan nya bersama sama yahhh. 
Oke sekali lagi Selamat ulang tahun.`;
    switchPage('page5');
}

function showGallery(){
    document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
    document.getElementById('pageGallery').style.display = 'block';
    document.body.style.overflowY = 'auto';
    window.scrollTo({top: 0, behavior: 'smooth'});
}

function showFinalMessage(){
    document.getElementById('pageGallery').style.display = 'none';
    switchPage('pageFinal');
    window.scrollTo({top: 0, behavior: 'smooth'});
    document.body.style.overflowY = 'hidden';
}

function kirimKeWA(){
    const pesan = document.getElementById('pesanWA').value;
    if(!pesan){
        alert("Tulis pesannya dulu dong 🤭");
        return;
    }
    const teksWA = `Halo! Aku ${userNama} (${userUmur}th). %0A%0AIni pesan dariku: %0A"${pesan}"`;
    window.open(`https://wa.me/${nomorWA}?text=${teksWA}`, '_blank');
}
</script>
</body>
</html>
""")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
