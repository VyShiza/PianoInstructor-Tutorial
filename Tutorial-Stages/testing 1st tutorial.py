import tkinter as tk
from tkinter import PhotoImage, Canvas, Tk
from PIL import Image, ImageTk
import pygame
from sampler import Sampler
import mido
import sys
import threading
import time
from pygame import mixer
from queue import Queue

root = tk.Tk()
root.title('Làm quen với C/D/E')

# --- Canvas Setup ---
canvas = tk.Canvas(root, width=1800, height=400, bg='#7CFC00')
canvas.pack()
canvas.focus_set()

# --- Musical Staff ---
num_lines = 5
line_spacing = 20
top_margin = 150
bass_top_margin = 250
White_box = canvas.create_rectangle(50, top_margin, 1550, top_margin + 100, fill='white')
for i in range(num_lines):
    y_position = top_margin + i * line_spacing
    canvas.create_line(50, y_position, 1550, y_position, fill='black', width=2)

# --- Clef ---
treble_clef = canvas.create_text(90, top_margin + 1.5 * line_spacing, text="𝄞", fill='black', font=("Segoe UI Symbol", 92))

# --- Cursor ---
cursor_end = canvas.create_rectangle(200, top_margin - 60, 205, bass_top_margin + 4 * line_spacing - 33, fill='cyan')
canvas.itemconfig(cursor_end, outline="", fill="")

# --- Note Definitions ---
note_regions = {
    "Do": (390, top_margin - 60, 410, bass_top_margin + 4 * line_spacing - 33),
    "Re": (745, top_margin - 60, 765, bass_top_margin + 4 * line_spacing - 33),
    "Mi": (1090, top_margin - 60, 1110, bass_top_margin + 4 * line_spacing - 33)
}

# --- Note Order and Message Handling ---
note_order = ["Do", "Re", "Mi"]
current_note_index = 0
mess1 = canvas.create_text(900, 300, text="Đặt ngón cái lên nút đầu tiên , nó là nốt Do hay gọi là C", fill='black', font=("Lucida Sans", 30))
def handle_message():
    global mess1, current_note_index

    if current_note_index == 1:
        canvas.delete(mess1)
        mess1 = canvas.create_text(900, 300, text="Tiếp theo là nút Re , nó là nốt D", fill='black', font=("Lucida Sans", 30))
    elif current_note_index == 2:
        canvas.delete(mess1)
        mess1 = canvas.create_text(900, 300, text="Cuối cùng là nốt Mi , nó là nốt E", fill='black', font=("Lucida Sans", 30))
    elif current_note_index == 3:
        canvas.delete(mess1)
        mess1 = canvas.create_text(900, 300, text="Bạn đã chơi xong 3 nốt! Bây giờ hãy thử lại nhé", fill='black', font=("Lucida Sans", 30))
        root.after(3000, lambda: canvas.delete(mess1))
        root.after(3000, end_program)
        current_note_index = 0  # Reset for the next round

# --- Block Handling ---
blocks = []
def create_block(note, time_to_appear, y_position):
    x_position = 2995 - time_to_appear * 50  # Vị trí x phụ thuộc vào thời gian xuất hiện
    block = canvas.create_text(x_position, y_position, text="♩", fill='black', font=("Segoe UI Symbol", 78), tags=(str(note),))
    blocks.append((block, y_position))
    #create_ledger_line(note, x_position, y_position, top_margin)

def create_ledger_line(note, x_position, y_position, top_margin):
    # Kiểm tra xem nốt có cần dòng kẻ phụ không
    if 220 > y_position > 210:
        ledger_line = canvas.create_line(x_position - 20, y_position + 30, x_position + 20, y_position + 30, fill='black', width=2, tags=(str(note),))
        blocks.append((ledger_line, y_position))
    if 230 > y_position > 220:
        ledger_line = canvas.create_line(x_position - 15, y_position + 20, x_position + 20, y_position + 20, fill='black', width=2, tags=(str(note),))
        blocks.append((ledger_line, y_position))
    if 240 > y_position > 230:
        ledger_line1 = canvas.create_line(x_position - 20, y_position + 30, x_position + 20, y_position + 30, fill='black', width=2, tags=(str(note),))
        ledger_line2 = canvas.create_line(x_position - 17, y_position + 10, x_position + 20, y_position + 10, fill='black', width=2, tags=(str(note),))
        blocks.append((ledger_line1, y_position))
        blocks.append((ledger_line2, y_position))

def is_note_item(item):
    tags = canvas.gettags(item)
    return 'note' in tags

# --- MIDI Input Handling ---
def midi_note():
    mixer.init()
    ignore_velocity = True if "--ignore_velocity" in sys.argv else False
    sustain = True if "--sustain" in sys.argv else False
    sampler = Sampler(mixer, ignore_velocity, sustain)
    global note_number
    port_name = 'Oxygen Pro 49 0'  # Replace with your MIDI port name
    while True:
        with mido.open_input(port_name) as port:
            for msg in port:
                try:
                    if msg.type == 'note_on':
                        note_number = msg.note
                        velocity = msg.velocity
                        sampler.play(note_id=note_number, vel=velocity)
                        print(note_number)
                        note_tag = str(note_number)
                        for block, y_position in blocks:
                            if note_tag in canvas.gettags(block):
                                canvas.delete(block)
                                blocks.remove((block, y_position))
                                global current_note_index
                                current_note_index += 1
                                handle_message()
                                break
                            break
                    elif msg.type == 'note_off':
                        note_number = msg.note
                        sampler.stop(note_id=note_number)
                except:
                    pass

# --- Other Functions ---
def note_to_position(note):
    note_positions = {
        '69': top_margin + 5.5 * line_spacing,  # a4
        '71': top_margin + 5 * line_spacing,  # b4
        '72': top_margin + 4.5 * line_spacing,  # c5
        '74': top_margin + 4 * line_spacing,  # d5
        '76': top_margin + 3.5 * line_spacing,  # e5
        '77': top_margin + 3 * line_spacing,  # f5
        '79': top_margin + 2.5 * line_spacing,  # g5
        '81': top_margin + 2 * line_spacing,  # a5
        '83': top_margin + 1.5 * line_spacing,  # b5
        '84': top_margin + 1 * line_spacing,  # c6
        '86': top_margin + 0.5 * line_spacing,  # d6
        '88': top_margin * line_spacing,  # e6
    }
    return note_positions.get(note, top_margin + 2 * line_spacing)

def create_blocks_from_sheet(sheet):
    for note_info in sheet:
        note, time_to_appear = note_info
        y_position = note_to_position(note)
        create_block(note, time_to_appear, y_position)

def reset_note_number():
    global note_number
    while True:
        time.sleep(0.2)
        note_number = -1

def update_end():
    # Lấy tọa độ của cursor
    cursor_coords = canvas.coords(cursor_end)
    # Tìm tất cả các items chồng lấp với cursor
    overlapping_items = canvas.find_overlapping(*cursor_coords)
    
    for item in overlapping_items:
        # Kiểm tra xem item có phải là nốt nhạc không (ví dụ: kiểm tra tag hoặc kiểu của item)
        if is_note_item(item):
            # Xóa item nốt nhạc khỏi canvas
            canvas.delete(item)
    canvas.after(100, update_end)

def check_end():
    remaining_notes = canvas.find_all
    if not remaining_notes:
        # Không còn nốt nhạc, gọi hàm end_program
        end_program()
    else:
        # Nếu vẫn còn nốt nhạc, tiếp tục kiểm tra sau mỗi khoảng thời gian
        canvas.after(100, check_end)

def end_program():
    canvas.create_text(900, 300, text="Finish", fill='black', font=("Segoe Script", 80))
    root.after(2000, root.destroy)

# --- Main Program ---
sheet_music = [
    ('72', 52), ('74', 45), ('76', 38)
]
create_blocks_from_sheet(sheet_music)

pygame.init()

reset_thread = threading.Thread(target=reset_note_number)
reset_thread.daemon = True
reset_thread.start()
midi_thread = threading.Thread(target=midi_note)
midi_thread.daemon = True
midi_thread.start()

update_end()
check_end()
root.mainloop()