import copy
import random
from pprint import pprint

from own_utils import get_blank_trees, ListDict, kill_descendants, kill_descendants

classname = "Holy Priest"
class_tree, spec_tree, class_unlocked, class_locked = get_blank_trees(
    classname
)  # list of strings? Also TODO see if this style of two results unpacking thingy is real or I just dreamed it up.
mandatory = set()
spec_unlocked = ListDict()
spec_locked = ListDict()
class_points = 31
spec_points = 30
spent_points = 0

for k, v in class_tree.items():
    spent_points += int(v["allocated"])

# Possible removal set
possible_removal = []
for k, v in class_tree.items():
    if v["mandatory"] == False:
        possible_removal.append(k)

# Build choices list.
raw_choices = []
side = "left"
for k, v in class_tree.items():
    if "locks" in v:
        raw_choices.append(k)

un_choices = []
for i in range(0, len(raw_choices), 2):
    if random.randint(0, 1) == 0:
        un_choices.append(raw_choices[i])
    else:
        un_choices.append(raw_choices[i + 1])

for i in un_choices:
    class_tree[i]["allocated"] = 0
    possible_removal.remove(i)

print(class_tree)
while spent_points > class_points:
    # Backups are for potential rollback if a chosen talent_to_remove ends up pruning too many children.
    # Reminder to add talent_to_remove to the mandatory list before rollback.
    # backup_class = copy.deepcopy(class_tree)
    # backup_spec_unlocked = copy.deepcopy(spec_unlocked)
    # backup_spec_locked = copy.deepcopy(spec_locked)
    # backup_possible_removal = copy.deepcopy(possible_removal)
    talent_to_remove = random.choice(possible_removal)
    print(talent_to_remove)
    class_tree[talent_to_remove]["allocated"] -= 1
    if (
        class_tree[talent_to_remove]["allocated"] < 0
    ):  # TODO 20251123: Figure out why talents keep going negative. Weirdness w/ kill_descendants()?
        pprint(class_tree)
        print(talent_to_remove)
        raise ValueError
    spent_points -= 1
    possible_removal, spent_points = kill_descendants(
        talent_to_remove, possible_removal, spent_points
    )

if spent_points == 31:
    for k, v in class_tree.items():
        if v["allocated"] != 0:
            print(f"{k}: {v["allocated"]} ranks")
else:
    print("Bad run!")


#     # Choose a random talent from the available list of class talents.
#     # Extremely naìve, will be rare to get capstones.
#     talent = class_unlocked.choose_random_item()
#     class_tree[talent]["allocated"] += 1
#     if class_tree[talent]["allocated"] == 1:
#         if "locks" in class_tree[talent]:
#             print(f"{talent} locks {class_tree[talent]["locks"]}")
#             class_locked.add_item(class_tree[talent]["locks"])
#             class_unlocked.remove_item(class_tree[talent]["locks"])
#     if class_tree[talent]["allocated"] == class_tree[talent]["max"]:
#         class_unlocked.remove_item(talent)
#         class_locked.add_item(talent)
#         for item in class_tree[talent]["unlocks"]:
#             if item not in class_locked:
#                 if spent_points >= class_tree[item]["total points required"]:
#                     class_unlocked.add_item(item)
#             else:
#                 print(f"{item} in {class_locked}")
#     spent_points += 1
# for talent in class_tree:
#     if class_tree[talent]["allocated"] == 1:
#         print(f"{talent} x1")
#     elif class_tree[talent]["allocated"] == 2:
#         print(f"{talent} x2")
