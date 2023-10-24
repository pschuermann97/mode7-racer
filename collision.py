# Module for everything related to collision.
# Note that we cannot the pygame built-in collision system
# since the shapes are not within screen space but within some custom logical 3D-space
# that pygame is not aware of.

# A class modelling a rectangular collider around a game object.
# A numpy list is used to model the colliders position.
class CollisionRect:
    def __init__(self, pos, w, h):
        self.position = pos
        self.width = w
        self.height = h

    # Determines whether this rectangle collider overlaps with the passed other one.
    def overlap(self, other):
        return (
            # x position close enough?
            abs(self.position[0] - other.position[0]) <= self.width / 2 + other.width / 2 and
            # y positions close enough?
            abs(self.position[1] - other.position[1]) <= self.height / 2 + other.height / 2
        )


    def __str__(self):
        return "(" + str(self.position[0]) + ", " + str(self.position[1]) + "), " + str(self.width) + ", " + str(self.height)