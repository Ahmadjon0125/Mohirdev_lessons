import asyncio
import edge_tts
from docx import Document

async def file_to_audio(file_path, output_file="output.mp3", rate=0):
    """TXT yoki DOCX fayldan audio yaratish"""
    
    # Matnni o'qish
    if file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        text = "\n".join([p.text for p in doc.paragraphs])
    else:
        return "Fayl turi noto'g'ri!"
    
    # Audioga o'girish
    rate_str = f"{rate:+.0f}%"
    communicate = edge_tts.Communicate(text=text, voice="en-US-GuyNeural", rate=rate_str)
    await communicate.save(output_file)
    
    print(f"✅ {output_file} saqlandi!")

# Foydalanish:
# asyncio.run(file_to_audio("matn.txt", "audio.mp3", rate=10))
asyncio.run(file_to_audio("text.txt", "audio.mp3", rate=-10))