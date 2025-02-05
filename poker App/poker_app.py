import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random
import os

class Player:
    def __init__(self, position):
        self.position = position
        self.hand = []

class Table:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = [Player(i) for i in range(1)]  # Solo un jugador
        self.initial_deck = self.create_deck()
        self.deck = self.initial_deck.copy()
        self.community_cards = []
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False

    def create_deck(self):
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        deck = [{'value': value, 'suit': suit} for suit in suits for value in values]
        random.shuffle(deck)
        print(f"Deck created with {len(deck)} cards")
        return deck

    def reset_deck(self):
        self.deck = self.initial_deck.copy()
        random.shuffle(self.deck)
        self.community_cards = []
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        print("Deck and community cards reset")

    def ensure_cards(self, num_required):
        if len(self.deck) < num_required:
            self.deck.extend(self.create_deck())
            random.shuffle(self.deck)
        print(f"Deck has {len(self.deck)} cards, {num_required} required")

    def burn_card(self):
        if self.deck:
            self.deck.pop()
            print(f"Burned a card, {len(self.deck)} cards left in deck")

    def deal_hands(self, hand1, hand2):
        self.players[0].hand = [hand1, hand2]
        print(f"Dealt hand to player: {self.players[0].hand}")

    def deal_flop(self):
        if self.flop_dealt:
            raise ValueError("El flop ya ha sido repartido.")
        self.ensure_cards(4)  # 1 quemar + 3 flop
        self.burn_card()  # Quemar una carta
        self.community_cards = [self.deck.pop() for _ in range(3)]  # Repartir el flop
        self.flop_dealt = True
        print(f"Dealt flop: {self.community_cards}, {len(self.deck)} cards left in deck")

    def deal_turn(self):
        if not self.flop_dealt:
            raise ValueError("Primero debe repartir el flop.")
        if self.turn_dealt:
            raise ValueError("El turn ya ha sido repartido.")
        self.ensure_cards(2)  # 1 quemar + 1 turn
        self.burn_card()  # Quemar una carta
        self.community_cards.append(self.deck.pop())  # Agregar el turn
        self.turn_dealt = True
        print(f"Dealt turn: {self.community_cards}, {len(self.deck)} cards left in deck")

    def deal_river(self):
        if not self.turn_dealt:
            raise ValueError("Primero debe repartir el turn.")
        if self.river_dealt:
            raise ValueError("El river ya ha sido repartido.")
        self.ensure_cards(2)  # 1 quemar + 1 river
        self.burn_card()  # Quemar una carta
        self.community_cards.append(self.deck.pop())  # Agregar el river
        self.river_dealt = True
        print(f"Dealt river: {self.community_cards}, {len(self.deck)} cards left in deck")

    def reset_community_cards(self):
        self.community_cards = []
        self.flop_dealt = False
        self.turn_dealt = False
        self.river_dealt = False
        print("Community cards reset")

    def change_flop(self):
        if not self.flop_dealt:
            raise ValueError("Primero debe repartir el flop.")
        self.ensure_cards(3)  # 3 flop
        self.community_cards[:3] = [self.deck.pop() for _ in range(3)]  # Cambiar el flop
        print(f"Changed flop: {self.community_cards}, {len(self.deck)} cards left in deck")

    def change_turn(self):
        if not self.turn_dealt:
            raise ValueError("Primero debe repartir el turn.")
        self.ensure_cards(1)  # 1 turn
        self.community_cards[3] = self.deck.pop()  # Cambiar el turn
        print(f"Changed turn: {self.community_cards}, {len(self.deck)} cards left in deck")

    def change_river(self):
        if not self.river_dealt:
            raise ValueError("Primero debe repartir el river.")
        self.ensure_cards(1)  # 1 river
        self.community_cards[4] = self.deck.pop()  # Cambiar el river
        print(f"Changed river: {self.community_cards}, {len(self.deck)} cards left in deck")

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Poker")
        self.table = Table(num_players=1)  # Solo un jugador

        # Definir los atributos 'suits' y 'values'
        self.suits = ['clubs', 'diamonds', 'hearts', 'spades']
        self.values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']

        # Cargar la imagen de fondo de la mesa de póker
        self.background_image = Image.open(os.path.join("backgrounds", "poker_table.png"))
        self.background_image = self.background_image.resize((800, 600), Image.Resampling.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

        # Crear un marco para los botones
        self.button_frame = ttk.Frame(root, padding="5")
        self.button_frame.pack(side="top", fill="x")

        # Crear botones con estilos ttk
        self.deal_flop_button = ttk.Button(self.button_frame, text="Flop", command=self.deal_flop)
        self.change_flop_button = ttk.Button(self.button_frame, text="Cambiar Flop", command=self.change_flop)
        self.deal_turn_button = ttk.Button(self.button_frame, text="Turn", command=self.deal_turn)
        self.change_turn_button = ttk.Button(self.button_frame, text="Cambiar Turn", command=self.change_turn)
        self.deal_river_button = ttk.Button(self.button_frame, text="River", command=self.deal_river)
        self.change_river_button = ttk.Button(self.button_frame, text="Cambiar River", command=self.change_river)
        self.reset_button = ttk.Button(self.button_frame, text="Resetear", command=self.reset_game)

        self.deal_flop_button.pack(side="left", padx=5, pady=5)
        self.change_flop_button.pack(side="left", padx=5, pady=5)
        self.deal_turn_button.pack(side="left", padx=5, pady=5)
        self.change_turn_button.pack(side="left", padx=5, pady=5)
        self.deal_river_button.pack(side="left", padx=5, pady=5)
        self.change_river_button.pack(side="left", padx=5, pady=5)
        self.reset_button.pack(side="left", padx=5, pady=5)

        # Crear etiquetas para el jugador
        self.players_labels = self.canvas.create_text(400, 100, text="Jugador: ", fill="white")

        self.card_images = {}  # Diccionario para almacenar las imágenes de las cartas
        self.small_card_images = {}  # Diccionario para almacenar las imágenes de las cartas en tamaño pequeño
        self.player_card_labels = []  # Lista para almacenar las etiquetas de las cartas del jugador
        self.community_card_labels = []  # Lista para almacenar las etiquetas de las cartas de la comunidad
        self.selected_cards = [None, None]  # Lista para almacenar las cartas seleccionadas
        self.load_card_images()

        # Dibujar el rectángulo hueco para alojar las "hold cards"
        offset_x = 56.6928  # Ajuste de 1.5 cm a la derecha
        hc1_x1, hc1_y1, hc1_x2, hc1_y2 = 280 + offset_x, 70, 280 + 63 + offset_x, 70 + 94
        hc2_x1, hc2_y1, hc2_x2, hc2_y2 = 280 + 63 + 10 + offset_x, 70, 280 + 2*63 + 10 + offset_x, 70 + 94
        self.hc1_rect = self.canvas.create_rectangle(hc1_x1, hc1_y1, hc1_x2, hc1_y2, outline="white", width=2)
        self.hc2_rect = self.canvas.create_rectangle(hc2_x1, hc2_y1, hc2_x2, hc2_y2, outline="white", width=2)
        self.canvas.tag_bind(self.hc1_rect, "<Button-1>", lambda e: self.show_card_selection(0))
        self.canvas.tag_bind(self.hc2_rect, "<Button-1>", lambda e: self.show_card_selection(1))
        
        # Crear botones HC1 y HC2
        self.hc1_button = tk.Button(self.canvas, text="HC1", command=lambda: self.show_card_selection(0), fg="black", font=("Helvetica", 10, "bold"))
        self.hc2_button = tk.Button(self.canvas, text="HC2", command=lambda: self.show_card_selection(1), fg="black", font=("Helvetica", 10, "bold"))
        self.canvas.create_window((hc1_x1 + hc1_x2) // 2, hc1_y1 - 20, window=self.hc1_button, anchor="center")
        self.canvas.create_window((hc2_x1 + hc2_x2) // 2, hc2_y1 - 20, window=self.hc2_button, anchor="center")

    def load_card_images(self):
        for suit in self.suits:
            for value in self.values:
                card_name = f"{value}_of_{suit}"
                image_path = os.path.join("PNG-cards-1.3", f"{card_name}.png")
                # Asegurarse de que la imagen exista antes de cargarla
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    # Cargar la imagen en tamaño original
                    original_image = image.resize((63, 94), Image.Resampling.LANCZOS)
                    self.card_images[card_name] = ImageTk.PhotoImage(original_image)
                    # Cargar la imagen en tamaño pequeño
                    small_image = image.resize((44, 66), Image.Resampling.LANCZOS)  # Redimensionar las imágenes un 30% más pequeñas
                    self.small_card_images[card_name] = ImageTk.PhotoImage(small_image)
                else:
                    print(f"Error: No se encontró la imagen {image_path}")

    def show_card_selection(self, card_index):
        # Crear una ventana emergente para seleccionar la carta
        self.popup = tk.Toplevel(self.root)
        self.popup.title("Seleccionar Carta")
        self.popup.geometry("600x400")
        self.popup.transient(self.root)

        for i, suit in enumerate(self.suits):
            for j, value in enumerate(self.values):
                card_name = f"{value}_of_{suit}"
                if card_name in self.small_card_images:
                    button = tk.Button(self.popup, image=self.small_card_images[card_name], command=lambda cn=card_name: self.select_card(card_index, cn))
                    button.grid(row=i, column=j, padx=5, pady=5)

    def select_card(self, card_index, card_name):
        # Asignar la carta seleccionada y actualizar la mano del jugador
        self.selected_cards[card_index] = card_name
        self.update_player_hands()
        self.popup.destroy()

    def show_error_message(self, message):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        tk.Label(error_window, text=message, padx=20, pady=10).pack()
        tk.Button(error_window, text="OK", command=error_window.destroy).pack(pady=5)

    def deal_flop(self):
        try:
            self.table.deal_flop()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def change_flop(self):
        try:
            self.table.change_flop()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def deal_turn(self):
        try:
            self.table.deal_turn()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def change_turn(self):
        try:
            self.table.change_turn()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def deal_river(self):
        try:
            self.table.deal_river()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def change_river(self):
        try:
            self.table.change_river()
            self.update_community_cards()
        except ValueError as e:
            self.show_error_message(str(e))

    def reset_game(self):
        self.table.reset_deck()
        self.selected_cards = [None, None]
        self.update_community_cards()
        self.update_player_hands()

    def update_player_hands(self):
        # Eliminar las cartas del jugador existentes
        for label in self.player_card_labels:
            self.canvas.delete(label)
        self.player_card_labels.clear()

        # Posicionar las cartas del jugador
        offset_x = 56.6928  # Ajuste de 1.5 cm a la derecha
        hc1_x1, hc1_y1, hc1_x2, hc1_y2 = 280 + offset_x, 70, 280 + 63 + offset_x, 70 + 94
        hc2_x1, hc2_y1, hc2_x2, hc2_y2 = 280 + 63 + 10 + offset_x, 70, 280 + 2*63 + 10 + offset_x, 70 + 94

        positions = [(hc1_x1, hc1_y1), (hc2_x1, hc2_y1)]

        for i, card_name in enumerate(self.selected_cards):
            if card_name:
                if card_name in self.card_images:
                    card_label = self.canvas.create_image(positions[i][0], positions[i][1], image=self.card_images[card_name], anchor="nw")
                    self.player_card_labels.append(card_label)

    def update_community_cards(self):
        # Eliminar las cartas de la comunidad existentes
        for label in self.community_card_labels:
            self.canvas.delete(label)
        self.community_card_labels.clear()

        # Posicionar las cartas de la comunidad (flop, turn, river)
        card_width = 63
        total_cards = len(self.table.community_cards)
        x_center = 400
        y_pos = 300  # Ajustar esta línea para bajar las cartas
        x_start = x_center - (total_cards * card_width + (total_cards - 1) * 10) // 2

        for i, card in enumerate(self.table.community_cards):
            card_name = f"{card['value']}_of_{card['suit']}"
            if card_name in self.card_images:
                card_label = self.canvas.create_image(x_start + i * (card_width + 10), y_pos, image=self.card_images[card_name], anchor="nw")
                self.community_card_labels.append(card_label)
            else:
                print(f"Error: No se encontró la imagen para {card_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()