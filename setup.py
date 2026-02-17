import os
import wave
import struct
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("ERRO: Instale o pillow -> pip install pillow")
    exit()

def create_folders():
    for folder in ['images', 'sounds', 'music']:
        os.makedirs(folder, exist_ok=True)

def create_sprite(name, color, size=40):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, size, size], fill=color)
    draw.rectangle([0, 0, size-1, size-1], outline="black")
    img.save(f"images/{name}.png")
    print(f"Criado: {name}.png")

def create_sound(name, folder="sounds"):
    path = f"{folder}/{name}"
    with wave.open(path, 'w') as f:
        f.setnchannels(1) 
        f.setsampwidth(2)
        f.setframerate(44100)
        data = struct.pack('<h', 0) * int(0.5 * 44100)
        f.writeframes(data)

def main():
    create_folders()
    sprites = {"hero": (0, 255, 0), "monster": (255, 100, 0), "boss": (255, 0, 0)}
    
    for tipo, cor in sprites.items():
        sz = 80 if tipo == "boss" else 40
        for i in range(4):
            create_sprite(f"{tipo}_idle_{i}", cor, sz)
            create_sprite(f"{tipo}_walk_{i}", cor, sz)

    for s in ["attack.wav", "click.wav", "game_over.wav", "level_up.wav", "victory.wav"]:
        create_sound(s, "sounds")
    create_sound("background.wav", "music")
    print("✅ Assets gerados com sucesso!")

if __name__ == "__main__":
    main()