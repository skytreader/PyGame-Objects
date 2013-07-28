class Collidable(object):
	"""
	Represents a game object that can collide with other game objects.
	
	Why not use the one built-in with pygame.sprite? This will allow us
	to implement better collision detection algorithms. Also, this allows
	us to attach collision detection non-sprite, irregular objects (e.g.,
	PointShapes).
	
	@author Chad Estioco
	"""
	
	def has_collided(collision_object):
		"""
		Determines whether two (Collidable) objects has collided
		with each other.
		"""
		pass
