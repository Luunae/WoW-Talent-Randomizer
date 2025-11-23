import random
from priestholy import holypriest_class_tree, holypriest_spec_tree


def get_blank_trees(classname):
    # TODO: Change ListDict so it accepts multiple items to be added at once, allowing for condensing multiple lines.
    class_unlocked = ListDict()
    class_locked = ListDict()
    # HOWTO: To add any new class add it as: elif classname == "Spec Class":
    # Set class_tree and spec_tree individually to the dictionaries representing that classpec.
    # Set the number of default allocated points for talents in your spec (e.g. HPriest starts off with free points in Renew and PoM.)
    # Add all talents that are *possible to purchase* on a fresh talent page or a full page reset to class_unlocked.
    # On the off chance your spec forces you into a specific choice node, put the *other* choice that you can't take into class_locked.
    # To get an overview of the structure of what I'm expecting, view /priestholy.py
    if classname == "Holy Priest":
        class_tree = holypriest_class_tree
        spec_tree = holypriest_spec_tree
        class_tree["Renew"]["allocated"] = 1
        class_tree["Prayer of Mending"]["allocated"] = 1
        class_unlocked.add_item("Dispel Magic")
        class_unlocked.add_item("Shadowfiend")
        class_unlocked.add_item("Improved Flash Heal")
        class_unlocked.add_item("Focused Mending")
        class_unlocked.add_item("Holy Nova")
        class_unlocked.add_item("Spell Warding")
        class_unlocked.add_item("Blessed Recovery")
    else:
        ValueError("Only Holy Priest is currently supported")
    return class_tree, spec_tree, class_unlocked, class_locked


def kill_descendants(
    talent: str, possible_removal: list, spent_points: int, tree=holypriest_class_tree
):
    print(spent_points)
    for descendant in tree[talent]["unlocks"]:
        if tree[descendant]["allocated"] != 0:
            has_parent = False
            for parent in tree[descendant]["parents"]:
                if tree[parent]["allocated"] == tree[talent]["max"]:
                    has_parent = True
            if not has_parent and tree[descendant]["allocated"] != 0:
                removed_points = tree[descendant]["allocated"]
                tree[descendant]["allocated"] = 0
                spent_points -= removed_points
                possible_removal.remove(descendant)
                possible_removal, spent_points = kill_descendants(
                    descendant, possible_removal, spent_points
                )
                continue
    return possible_removal, spent_points


class ListDict(object):  # https://stackoverflow.com/a/15993515
    def __init__(self):
        self.item_to_position = {}
        self.items = []

    def __contains__(self, item):
        return item in self.item_to_position

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def add_item(self, item):
        if item in self.item_to_position:
            return
        self.items.append(item)
        self.item_to_position[item] = len(self.items) - 1

    def remove_item(self, item):
        position = self.item_to_position.pop(item)
        last_item = self.items.pop()
        if position != len(self.items):
            self.items[position] = last_item
            self.item_to_position[last_item] = position

    def choose_random_item(self):
        return random.choice(self.items)
