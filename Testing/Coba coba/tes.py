from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

# Inisialisasi Game
app = Ursina()

# Jenis Tekstur Blok (Menggunakan tekstur bawaan Ursina)
block_textures = {"1": "grass", "2": "stone", "3": "brick", "4": "dirt"}
current_texture = "grass"


# Kelas untuk Blok Kubus
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture="grass"):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1,
        )

    # Deteksi Input Mouse
    def input(self, key):
        if self.hovered:
            # Klik Kanan: Pasang Blok Baru
            if key == "right mouse down":
                voxel = Voxel(
                    position=self.position + mouse.normal, texture=current_texture
                )

            # Klik Kiri: Hancurkan Blok
            if key == "left mouse down":
                destroy(self)


# Mengubah jenis blok saat tombol 1-4 ditekan
def update():
    global current_texture
    if held_keys["1"]:
        current_texture = block_textures["1"]
    if held_keys["2"]:
        current_texture = block_textures["2"]
    if held_keys["3"]:
        current_texture = block_textures["3"]
    if held_keys["4"]:
        current_texture = block_textures["4"]


# Membuat Tanah (Ukuran 16x16 blok)
for z in range(16):
    for x in range(16):
        voxel = Voxel(position=(x, 0, z))

# Karakter Pemain (Kamera Orang Pertama)
player = FirstPersonController()
player.cursor.visible = True  # Menampilkan crosshair di tengah

# Jalankan Game
app.run()
