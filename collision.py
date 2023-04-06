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
            self.position[1] + self.height > other.position[1] - other.height # overlapping with a rectangle above
            or self.position[0] + self.width > other.position[0] - other.width # overlapping w. a. r. right
            or self.position[1] - self.height < other.position[1] + other.height # overlapping w. a. r. below
            or self.position[0] - self.width < other.position[0] + other.width # overlapping with w. a. r. left
        )