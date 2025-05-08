class RawMaterialsDto: 
  def __init__(self, name: str, unity: str, quantity_stock: float):
    self.name = str(name)
    self.unity = str(unity) # KG, TL
    self.quantity = float(quantity_stock)