import asyncio
import edge_tts
import os
from pathlib import Path
from docx import Document
from edge_tts import VoicesManager

async def interactive_file_converter():
    print("=" * 60)
    print("🎙️ FILE TO MP3 CONVERTER (Erkak ovozi)")
    print("=" * 60)
    
    # 1. Faylni tanlash
    print("\n📁 Qaysi faylni aylantirmoqchisiz?")
    print("   Masalan: matn.txt yoki hujjat.docx")
    input_file = input("Fayl nomi: ").strip()
    
    if not os.path.exists(input_file):
        print(f"❌ {input_file} topilmadi!")
        return
    
    # 2. Matnni o'qish
    file_ext = Path(input_file).suffix.lower()
    if file_ext == '.txt':
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_ext == '.docx':
        doc = Document(input_file)
        text = '\n'.join([p.text for p in doc.paragraphs])
    else:
        print("❌ Faqat .txt yoki .docx qo'llab-quvvatlanadi")
        return
    
    print(f"✅ {len(text)} belgi o'qildi")
    
    # 3. Ovoz tanlash
    voices = await VoicesManager.create()
    male_voices = voices.find(Language="en", Gender="Male")
    
    print("\n🎤 Eng yaxshi erkak ovozlari:")
    top_voices = [
        "en-US-GuyNeural",
        "en-US-DavisNeural", 
        "en-US-TonyNeural",
        "en-GB-RyanNeural",
        "en-AU-WilliamNeural"
    ]
    
    for i, voice in enumerate(top_voices, 1):
        print(f"   {i}. {voice}")
    
    choice = input("\nOvozni tanlang (1-5) yoki Enter (1-ovoz): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= 5:
        voice = top_voices[int(choice)-1]
    else:
        voice = "en-US-GuyNeural"
    
    # 4. Tezlik
    print("\n⚡ Tezlik:")
    print("   1 - Sekinroq (-15%)")
    print("   2 - Normal (0%)")
    print("   3 - Tezroq (+15%)")
    print("   4 - Juda sekin (-40%)")
    print("   5 - Juda tez (+40%)")
    
    speed_choice = input("Tanlang (1-5): ").strip()
    speed_map = {
        "1": "-15%", "2": "+0%", "3": "+15%",
        "4": "-40%", "5": "+40%"
    }
    rate = speed_map.get(speed_choice, "+0%")
    
    # 5. Ohang
    print("\n🎵 Ohang:")
    print("   1 - Pastroq")
    print("   2 - Normal")
    print("   3 - Balandroq")
    
    pitch_choice = input("Tanlang (1-3): ").strip()
    pitch_map = {"1": "-8Hz", "2": "+0Hz", "3": "+8Hz"}
    pitch = pitch_map.get(pitch_choice, "+0Hz")
    
    # 6. Chiqish fayli
    default_name = Path(input_file).stem + "_audio.mp3"
    output_file = input(f"\n💾 Chiqish fayli (Enter = {default_name}): ").strip()
    if not output_file:
        output_file = default_name
    if not output_file.endswith('.mp3'):
        output_file += '.mp3'
    
    # 7. Yaratish
    print(f"\n⏳ Yaratilmoqda... (bu bir necha daqiqa vaqt olishi mumkin)")
    
    # Matnni bo'laklash
    chunk_size = 4500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    if len(chunks) == 1:
        tts = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await tts.save(output_file)
    else:
        print(f"   📦 {len(chunks)} ta bo'lakka ajratildi...")
        temp_files = []
        for i, chunk in enumerate(chunks):
            temp_file = f"temp_{i}.mp3"
            temp_files.append(temp_file)
            tts = edge_tts.Communicate(chunk, voice, rate=rate, pitch=pitch)
            await tts.save(temp_file)
            print(f"   ✅ Bo'lak {i+1}/{len(chunks)}")
        
        # Birlashtirish (ffmpeg kerak)
        with open('merge_list.txt', 'w') as f:
            for tf in temp_files:
                f.write(f"file '{os.path.abspath(tf)}'\n")
        
        import subprocess
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0',
            '-i', 'merge_list.txt', '-c', 'copy', output_file
        ], capture_output=True)
        
        for tf in temp_files:
            os.remove(tf)
        os.remove('merge_list.txt')
    
    print(f"\n✅ {output_file} saqlandi!")
    print(f"   Ovoz: {voice}")
    print(f"   Tezlik: {rate}")
    print(f"   Ohang: {pitch}")
    print(f"   Hajmi: {os.path.getsize(output_file) / (1024*1024):.2f} MB")

# Ishga tushirish
asyncio.run(interactive_file_converter())