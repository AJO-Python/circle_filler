#-*-coding: UTF-8-*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class Circle_obj:
    """
    Creates a circle object that can tell if it overlaps another circle or
    is outside a given region
    """
    def __init__(self, size, location):
        self.size = size
        self.loc = np.asarray(location)
        self.radius = size/2
        self.color = "r"

    def make_patch(self):
        """
        For use with ax.add_patch()
        :return: A matplotlib patch object
        """
        return Circle(
            xy=self.loc,
            radius=self.radius,
            facecolor=self.color,
            linewidth=3,
            edgecolor="k"
        )

    def is_touching(self, other):
        """
        Checks if circles are touching
        :param Circle_obj other: Circle to check overlap with
        :rtype: bool
        :return: True if circles overlap
        """
        distance = np.linalg.norm(other.loc - self.loc)
        if distance < (self.radius + other.radius):
            return True
        else:
            return False

    def is_out_region(self, region):
        """
        Checks if circle is outside of the defined region
        :param tuple(int, int) region: Width and height of region
        :rtype: bool
        :return: True if Circle is outside of region
        """
        r = self.radius
        if (self.loc[0] - r < 0) or ((self.loc[0]+r) > region[0]):
            return True
        elif (self.loc[1] - r < 0) or ((self.loc[1]+r) > region[1]):
            return True
        else:
            return False

def fill_with_circles(size, region_size, patience):
    """
    :param int size: width of max circle size
    :param tuple(int, int) region_size: fill area (pixels)
    :rtype: list(object)
    :return: list of Cirles to fill region
    """
    circles = []
    minimum_size = 5
    overlap_count = 0

    # Continue making circles until minimum size reached
    while size >= minimum_size:
        x = np.random.randint(region_size[0])
        y = np.random.randint(region_size[1])
        location = [x, y]
        # Make a new test circle
        new_circle = Circle_obj(size, location)
        # If it overlaps with any existing circles then dont add it
        overlaps = [new_circle.is_touching(other) for other in circles]
        if np.any(overlaps):
            overlap_count += 1
        # If it has its own space add to list
        elif new_circle.is_out_region(region_size):
            overlap_count += 1
        else:
            circles.append(new_circle)
            # Reset overlap count
            overlap_count = 0

        # If no new circles have been added then decrease the size and
        # reset the overlap count
        if overlap_count % patience == 0:
            size -= minimum_size
            print(f"Size: {size}")
            overlap_count = 0

    return circles

def plot_circles(circle_list):
    """
    :param list(Circle) circle_list: List of Circles to add to a plot
    :return: fig, ax
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    for circle in circle_list:
        patch = circle.make_patch()
        ax.add_patch(patch)
        #ax.annotate(f"{circle.size}", xy=circle.loc)
    return fig, ax

def main():
    print("Inside main function")

    print("Set starting size and region")
    starting_size = 250
    region = [600, 400]
    patience = 5_000

    print("Filling with circles")
    circles = fill_with_circles(starting_size, region, patience)

    print("Adding circles to plot")
    fig, ax = plot_circles(circles)

    # Format plot
    ax.set_xlim(0, region[0])
    ax.set_ylim(0, region[1])
    ax.set_aspect("equal")

    print("Saving figure...")
    fig.savefig("circles.png", bbox_inches="tight", dpi=1600)
    print("Finished.")

if __name__ == "__main__":
    main()