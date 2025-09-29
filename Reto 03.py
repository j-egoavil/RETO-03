class MenuItem:
    # Clase base para todos los items del menú.
    
    def __init__(self, nombre: str, precio: float):
        self.nombre = nombre
        self.precio = precio
    
    def get_total(self) -> float:
        # Calcular precio total para este item.
        return self.precio
    
    def __str__(self) -> str:
        return f"{self.nombre}: ${self.precio:.2f}"

class Bebida(MenuItem):
    # Bebida con opción de tamaño.
    
    def __init__(self, nombre: str, precio: float, tamaño: str = "regular"):
        super().__init__(nombre, precio)
        self.tamaño = tamaño
        
        # Ajustar precio basado en el tamaño
        if tamaño == "pequeño":
            self.precio = precio * 0.8
        elif tamaño == "grande":
            self.precio = precio * 1.3
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.tamaño}): ${self.precio:.2f}"

class Entrada(MenuItem):
    # Entradas con opción para compartir.
    
    def __init__(self, nombre: str, precio: float, compartido: bool = False):
        super().__init__(nombre, precio)
        self.compartido = compartido
    
    def __str__(self) -> str:
        info_compartir = " (para compartir)" if self.compartido else ""
        return f"{self.nombre}{info_compartir}: ${self.precio:.2f}"

class PlatoPrincipal(MenuItem):
    # plato principal con tipo de proteína.
    
    def __init__(self, nombre: str, precio: float, proteina: str):
        super().__init__(nombre, precio)
        self.proteina = proteina
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.proteina}): ${self.precio:.2f}"

class Pedido:
    
    def __init__(self, numero_mesa: int):
        self.numero_mesa = numero_mesa
        self.items = []
    
    def agregar_item(self, item: MenuItem) -> None:
        self.items.append(item)
    
    def get_subtotal(self) -> float:
        # Calcular subtotal antes de descuentos.
        return sum(item.get_total() for item in self.items)
    
    def aplicar_descuento(self, subtotal: float) -> tuple:
        """
        Aplicar descuentos basados en la composición del pedido.
        Retorna: (monto_descuento, razon_descuento)
        """
        # Verificar descuento de bebida (bebida gratis por pedido de mas de $25)
        tiene_plato_principal = any(isinstance(item, PlatoPrincipal) for item in self.items)
        contador_bebidas = sum(1 for item in self.items if isinstance(item, Bebida))
        
        if tiene_plato_principal and subtotal > 25 and contador_bebidas > 0:
            # Encontrar la bebida más barata
            bebidas = [item for item in self.items if isinstance(item, Bebida)]
            if bebidas:
                bebida_mas_barata = min(bebidas, key=lambda x: x.precio)
                return bebida_mas_barata.precio, "Bebida gratis por pedido de mas de $25"
        
        return 0.0, "No se aplicó descuento"
    
    def get_total(self) -> float:
        # Calcular total final después de descuentos.
        subtotal = self.get_subtotal()
        monto_descuento, razon_descuento = self.aplicar_descuento(subtotal)
        return subtotal - monto_descuento
    
    def mostrar_factura(self) -> None:
        # Mostrar la factura formateada.
        print(f"\n{'='*50}")
        print(f"MESA {self.numero_mesa} - FACTURA FINAL")
        print(f"{'='*50}")
        
        for i, item in enumerate(self.items, 1):
            print(f"{i:2d}. {item}")
        
        subtotal = self.get_subtotal()
        monto_descuento, razon_descuento = self.aplicar_descuento(subtotal)
        propina = subtotal * 0.05  # 5% de propina
        total_final = subtotal - monto_descuento + propina
        
        print(f"\n{'='*50}")
        print(f"Subtotal: ${subtotal:.2f}")
        if monto_descuento > 0:
            print(f"Descuento: -${monto_descuento:.2f} ({razon_descuento})")
        print(f"propina (5%): ${propina:.2f}")
        print(f"{'-'*50}")
        print(f"TOTAL: ${total_final:.2f}")
        print(f"{'='*50}")

def crear_menu():
    menu = [
        # Bebidas
        Bebida("Coca-Cola", 2.50, "regular"),
        Bebida("Té Helado", 2.25, "regular"),
        Bebida("Café", 2.00, "regular"),
        Bebida("Jugo de Naranja Natural", 4.50, "grande"),
        Bebida("Agua Mineral", 1.50, "pequeño"),
        
        # Entradas
        Entrada("Palitos de Mozzarella", 8.99),
        Entrada("Alitas de Pollo", 12.99, True),
        Entrada("Pan de Ajo", 5.99),
        Entrada("Nachos", 10.99, True),
        Entrada("Sopa del Día", 6.99),
        
        # Platos Principales
        PlatoPrincipal("Salmón a la Parrilla", 22.99, "salmón"),
        PlatoPrincipal("Filete Ribeye", 28.99, "res"),
        PlatoPrincipal("Pollo a la Parmesana", 18.99, "pollo"),
        PlatoPrincipal("Pasta Vegetariana", 16.99, "vegetariano"),
        PlatoPrincipal("Hamburguesa BBQ", 15.99, "res"),
        PlatoPrincipal("Ensalada César", 12.99, "pollo"),
        PlatoPrincipal("Lasagna", 17.99, "res"),
        PlatoPrincipal("Pescado del Día", 24.99, "pescado")
    ]
    return menu

def mostrar_menu(menu):
    """Mostrar el menú disponible."""
    print(f"\n{'='*40}")
    print("MENÚ DEL RESTAURANTE")
    print(f"{'='*40}")
    
    print("\n--- BEBIDAS ---")
    for i, item in enumerate(menu[:5], 1):
        print(f"{i:2d}. {item}")
    
    print("\n--- ENTRADAS ---")
    for i, item in enumerate(menu[5:10], 6):
        print(f"{i:2d}. {item}")
    
    print("\n--- PLATOS PRINCIPALES ---")
    for i, item in enumerate(menu[10:], 11):
        print(f"{i:2d}. {item}")

def demo_sistema():
    # Crear menú
    menu = crear_menu()
    
    # Mostrar menú disponible
    mostrar_menu(menu)
    
    # Crear un pedido de ejemplo
    pedido1 = Pedido(numero_mesa=5)

    # Agregar items al pedido (simulando una orden real)
    pedido1.agregar_item(menu[5])   # Palitos de Mozzarella
    pedido1.agregar_item(menu[6])   # Alitas de Pollo (compartido)
    pedido1.agregar_item(menu[10])  # Salmón a la Parrilla
    pedido1.agregar_item(menu[0])   # Coca-Cola
    pedido1.agregar_item(menu[4])   # Agua mineral
    pedido1.agregar_item(menu[15])  # Ensalada César
    
    pedido1.mostrar_factura()

demo_sistema()