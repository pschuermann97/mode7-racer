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
        # case 1: other rectangle's center is located to the left of this rectangle
        if other.position[0] <= self.position[0]:
            # check whether the horizontal coordinates allow for an overlap
            if self.position[0] - self.width / 2 <= other.position[0] + other.width / 2:
                # case 1.1: located to the lower left of this rectangle
                if other.position[1] <= self.position[1]:
                    return self.position[1] - self.height / 2 <= other.position[1] + other.height / 2
                # case 1.2: located to the upper left of this rectangle
                else:
                    return self.position[1] + self.height / 2 >= other.position[1] - other.height / 2
        # case 2: other rectangle's center is located to the right of this rectangle
        else:
            # check whether the horizontal coordinates allow for an overlap
            if self.position[0] + self.width / 2 >= other.position[0] - other.width / 2:
                # case 1.1: located to the lower left of this rectangle
                if other.position[1] <= self.position[1]:
                    return self.position[1] - self.height / 2 <= other.position[1] + other.height / 2
                # case 1.2: located to the upper left of this rectangle
                else:
                    return self.position[1] + self.height / 2 >= other.position[1] - other.height / 2


    def __str__(self):
        return "(" + str(self.position[0]) + ", " + str(self.position[1]) + "), " + str(self.width) + ", " + str(self.height)