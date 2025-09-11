class Cell:
  def __init__(self):
    self.has_mine: bool = False
    self.has_flag: bool = False

  def flag(self):
    self.has_flag = True

  def unflag(self):
    self.has_flag = False

  def add_mine(self):
      self.has_mine = True

  def remove_mine(self):
    self.has_mine = False

